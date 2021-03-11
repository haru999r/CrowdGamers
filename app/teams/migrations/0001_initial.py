# Generated by Django 3.1.5 on 2021-03-11 07:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import teams.utils.model_validation
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('feature', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '特徴',
                'verbose_name_plural': '特徴',
                'db_table': 't_feature',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'ゲーム',
                'verbose_name_plural': 'ゲーム',
                'db_table': 't_game',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('job', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'ジョブ',
                'verbose_name_plural': 'ジョブ',
                'db_table': 't_job',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=255)),
                ('awnser', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'よくある質問',
                'verbose_name_plural': 'よくある質問',
                'db_table': 't_question',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('teamname', models.CharField(db_index=True, max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='[a-xA-Z0-9_]')], verbose_name='チームネーム')),
                ('name', models.CharField(max_length=100)),
                ('header', models.ImageField(blank=True, default='default/profile_header.jpg', upload_to=teams.utils.model_validation.user_directory_path, validators=[teams.utils.model_validation.validate_icon_image])),
                ('icon', models.ImageField(blank=True, default='default/profile_icon.png', upload_to=teams.utils.model_validation.user_directory_path, validators=[teams.utils.model_validation.validate_icon_image])),
                ('url', models.URLField(blank=True, null=True)),
                ('description', models.CharField(max_length=255)),
                ('sponsor', models.CharField(blank=True, max_length=100, null=True)),
                ('desired_condition', models.CharField(max_length=200)),
                ('disclosed', models.BooleanField(verbose_name='公開・非公開')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desired_job', models.ManyToManyField(related_name='team_desired_job', to='teams.Job')),
                ('feature', models.ManyToManyField(related_name='team_feature', to='teams.Feature', verbose_name='特徴')),
                ('game_title', models.ManyToManyField(related_name='team_game_title', to='teams.Game')),
            ],
            options={
                'verbose_name': 'チーム',
                'verbose_name_plural': 'チーム',
                'db_table': 't_team',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='ニックネーム', max_length=100, verbose_name='ニックネーム')),
                ('icon', models.ImageField(blank=True, default='default/profile_icon.png', upload_to=teams.utils.model_validation.user_directory_path, validators=[teams.utils.model_validation.validate_icon_image])),
                ('header', models.ImageField(blank=True, default='default/profile_header.jpg', upload_to=teams.utils.model_validation.user_directory_path, validators=[teams.utils.model_validation.validate_header_image])),
                ('is_owner', models.BooleanField(default=False)),
                ('introduction', models.CharField(blank=True, max_length=140, null=True)),
                ('clip_url', models.URLField(blank=True, null=True)),
                ('desired_condition', models.CharField(max_length=255, verbose_name='希望条件')),
                ('disclosed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desired_job', models.ManyToManyField(related_name='profile_desired_job', to='teams.Job')),
                ('feature', models.ManyToManyField(related_name='profile_feature', to='teams.Feature')),
                ('game_title', models.ManyToManyField(related_name='user_game_title', to='teams.Game')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='belonging_user_profiles', to='teams.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ユーザープロフィール',
                'verbose_name_plural': 'ユーザープロフィール',
                'db_table': 't_user_profile',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mode', models.CharField(choices=[('application', 'リクエスト'), ('invitation', '招待'), ('member_approval', 'メンバー追加'), ('official', '公式')], max_length=50)),
                ('invite_url', models.URLField(null=True, verbose_name='招待URL')),
                ('message', models.CharField(max_length=255)),
                ('has_read', models.BooleanField(default=False, verbose_name='既読')),
                ('is_proceeded', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('desired_job', models.ManyToManyField(related_name='invite_desired_job', to='teams.Job')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '通知',
                'verbose_name_plural': '通知',
                'db_table': 't_notification',
            },
        ),
    ]
