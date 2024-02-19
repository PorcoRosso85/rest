import pytest
from django.db.models.signals import pre_save
from django.dispatch import receiver

from app.models import PublishmentStatus
from app.utils import logger


@receiver(pre_save, sender=PublishmentStatus)
def handler_publishment_status(sender, instance, **kwargs):
    if instance.status == "":
        raise Exception("status is required")
    logger.info("publishment status is valid")


@pytest.mark.django_db
def test_正常系_バリデーションが成功する場合():
    """バリデーションが成功する場合"""
    status = PublishmentStatus(status="published")
    status.save()
    assert status.status == "published"


@pytest.mark.django_db
def test_異常系_バリデーションが失敗する場合():
    """バリデーションが失敗する場合"""
    with pytest.raises(Exception):
        PublishmentStatus(status="").save()
