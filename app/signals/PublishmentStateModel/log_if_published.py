import pytest
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from app.models import PublishmentStatus
from app.utils import logger


@receiver(post_save, sender=PublishmentStatus)
def log_if_published(sender, instance, **kwargs):
    if instance.status == instance.STATUS_OPTIONS[2][0]:
        instance.data._published_at = timezone.now()
        instance.data.save()
        logger.info(f"# status is {instance.status}")
        logger.info(f"# published_at is {instance.data._published_at}")
        logger.info("published_at is added")
    else:
        pass


class TestLogIfPublished:
    @pytest.mark.django_db
    def test_正常系_ログが出力される場合(self):
        """ログが出力される場合"""
        status = PublishmentStatus.objects.create(status="published")
        assert status.status == "published"
