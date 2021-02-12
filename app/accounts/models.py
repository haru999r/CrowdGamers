from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
import uuid



class CustomUserManager(UserManager):
    """ ユーザーマネージャー """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class User(AbstractBaseUser, PermissionsMixin):
    """ カスタムユーザー """

    def validate_icon_image(fieldfile_obj):
        image_size = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if image_size > megabyte_limit*1024*1024:
            raise ValidationError("ファイルのサイズを%sMBより小さくしてください" % str(megabyte_limit))

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username_regex = RegexValidator(regex=r'[a-xA-Z0-9_]')
    username = models.CharField(
        verbose_name='ユーザーネーム',
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        max_length=15,
        validators=[MinLengthValidator(4), username_regex])
    name = models.CharField(verbose_name='ニックネーム', max_length=100)
    icon = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        validators=[
            validate_icon_image,
        ])
    age = models.IntegerField(
            verbose_name='年齢',
            validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    # superuser を作るときの必須フィールド
    REQUIRED_FIELDS = ['username', 'age']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):

        # このユーザーにメールを送信する
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        username を返す
        """
        return self.username

@receiver(post_save, sender=User)
def create_user_clan(sender, **kwargs):
    # 新規ユーザー作成時に UserClan モデルの空インスタンスを生成
    if kwargs['created']:
        user_clan = clans.models.UserClan.objects.get_or_create(user=kwargs['instance'])
