import pytest
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from app.models import Data
from app.utils import logger


@receiver(pre_save, sender=Data)
def presave_signal_data(sender, instance, **kwargs):
    # craeted_atを追加する
    if instance._created_at is None:
        instance._created_at = timezone.now()
    logger.info("data is valid")

    # valueが空の場合はエラー
    if instance.value == {}:
        raise Exception("value is required")
    logger.info("data is valid")

    # updated_atを更新する
    instance._updated_at = timezone.now()


class TestPreSaveSignalData:
    @pytest.fixture
    def fixture_data(self):
        return Data.objects.create(value={"key": "value"})

    @pytest.mark.django_db
    def test_正常系_日付が追加された(self, fixture_data):
        assert fixture_data._created_at is not None
        assert fixture_data._updated_at is not None

    @pytest.mark.django_db
    def test_正常系_バリデーションが成功する場合(self, fixture_data):
        """バリデーションが成功する場合"""
        assert fixture_data.value == {"key": "value"}

    @pytest.mark.django_db
    def test_異常系_バリデーションが失敗する場合(self):
        """バリデーションが失敗する場合"""
        with pytest.raises(Exception):
            Data(value={}).save()
