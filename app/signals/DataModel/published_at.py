"""
このファイルは
DataModelのpublished_atに関するシグナルを管理するファイルです。
published_atフィールドは
デフォルトでnull=True, blank=Trueですが、
該当DataのPublishmentStatusがpublishedの場合、
published_atに値が入ります。
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from app.models import Data, PublishmentStatus
from app.utils import logger


@receiver(post_save, sender=Data)
def fill_published_at(sender, instance, created, **kwargs):
    logger.debug("!!! fill_published_at")
    instance._published_at = timezone.now()


import pytest


class TestFillPublishedAt:
    @pytest.mark.django_db
    def test_正常系_シグナルが発火する(self):
        _data = Data.objects.create()
        publishment_status = PublishmentStatus.objects.create(
            _data=_data, status="published"
        )
        _data.save()
        publishment_status.save()
        assert _data.id == publishment_status._data.id
        assert _data._published_at is not None
        # assert _data._published_at == snapshot(
        #     datetime.datetime(
        #         2024, 2, 21, 6, 6, 15, 604456, tzinfo=datetime.timezone.utc
        #     )
        # )
