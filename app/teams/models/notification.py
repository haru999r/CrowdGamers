from django.db import models
from django.contrib.auth import get_user_model
from .job import Job
import uuid



class Notification(models.Model):
    """
    通知関係を管理する

    MODE
    -----
    application : チームリクエスト
    invitation : 個人への招待
    member_approval : チーム登録の申請
    official : 公式情報

    Notes
    -----
    has_read は既読管理
    is_proceeded は承認・拒否管理

    TODO
    -----
    accounts.models の最初の通知のクラスを変更する
    """
    class Meta():
        db_table = 't_notification'
        verbose_name = '通知'
        verbose_name_plural = '通知'

    MODE = (
        ('application', 'リクエスト'),
        ('invitation', '招待'),
        ('member_approval', 'メンバー追加'),
        ('official', '公式'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, db_index=True)
    mode = models.CharField(
        choices=MODE,
        max_length=50,
    )
    from_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='sender',
    )
    to_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reciever',
    )
    desired_job = models.ManyToManyField(Job, related_name='invitation_desired_job')
    invitation_url = models.URLField(verbose_name='招待URL', null=True)
    message = models.CharField(max_length=255, null=False, blank=False)
    has_read = models.BooleanField(verbose_name='既読', default=False)
    is_proceeded = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
