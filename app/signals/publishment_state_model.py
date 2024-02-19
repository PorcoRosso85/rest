import pytest
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from app.models import Data, PublishmentStatus
from app.utils import logger


@receiver(post_save, sender=PublishmentStatus)
def postsave_signal_publishmentstate(sender, instance, **kwargs):
    if instance.status == "":
        raise Exception("status is required")
    logger.info("publishment status is valid")

    # ここでpublishment_statusがpublishedの場合は、Dataインスタンスのpublished_atを追加する
    if (
        instance.status == "published"
        and instance.status != instance.__class__.objects.get(pk=instance.pk).status
    ):
        instance.data._published_at = timezone.now()
        instance.data.save()
        logger.info("published_at is added")


class TestPostSaveSignalPublishmentStatus:
    @pytest.mark.django_db
    def test_正常系_バリデーションが成功する場合(self):
        """バリデーションが成功する場合"""
        value = {"key": "value"}
        data = Data.objects.create(value=value)
        status = PublishmentStatus.objects.create(data=data, status="published")
        status.save()
        assert status.status == "published"

    @pytest.mark.django_db
    def test_異常系_バリデーションが失敗する場合(self):
        """バリデーションが失敗する場合"""
        with pytest.raises(Exception):
            PublishmentStatus(status="").save()
