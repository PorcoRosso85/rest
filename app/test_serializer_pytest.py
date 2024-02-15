import pytest
from inline_snapshot import snapshot
from rest_framework.exceptions import ErrorDetail

from app.models import Content, Space, Status
from app.serializer import ContentSerializer, SpaceSerializer, StatusSerializer


class TestStatusModel:
    def setup_method(self):
        self.status = Status.objects.create(status="draft")

    @pytest.mark.django_db
    def test_status_model(self):
        assert self.status
        assert self.status.status == "draft"
        assert self.status.status != "published"


class TestStatusSerializer:
    @pytest.mark.django_db
    def test_status_serializer_draft(self):
        self.status = Status.objects.create(status="draft")
        assert self.status.status == "draft"
        serializer = StatusSerializer(data={"status": "draft"})
        serializer.is_valid()

    @pytest.mark.django_db
    def test_オプションのみを許容するバリデーション(self):
        self.status = Status.objects.create(status="")
        assert self.status.status == ""
        serializer = StatusSerializer(data={"status": ""})
        serializer.is_valid()
        # is_valid()で期待するエラーであることを確認したい、エラー理由は"status is required"
        assert serializer.is_valid() is False
        assert serializer.errors == snapshot(
            {
                "status": [
                    ErrorDetail(
                        string='"" is not a valid choice.', code="invalid_choice"
                    )
                ]
            }
        )
        assert serializer.data == {"status": ""}


class TestContentSerializer:
    def setup_method(self):
        self.status = Status.objects.create(status="draft")
        self.content = Content.objects.create(title="Test Content", status=self.status)

    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        # Serializerを作成
        serializer = ContentSerializer(self.content)
        assert serializer.data == snapshot(
            {
                "id": self.content.id,
                "title": "Test Content",
                "created_at": self.content.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": self.content.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "published_at": self.content.published_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "model": None,
                "status": self.status.id,
            }
        )


class TestSpaceSerializer:
    """
    jsonを返すシリアライザのテスト
    jsonのうちdata[]は、ContentSerializerでテストされている
    ContentSerializerから返されるデータをdata[]に入れてテストする
    SpaceモデルはContentモデルと1対多の関係にある、Contentモデルを参照している
    """

    def setup_method(self):
        self.space = Space.objects.create(name="Test Space")
        self.status = Status.objects.create(status="draft")
        self.content = Content.objects.create(title="Test Content", status=self.status)
        # SpaceインスタンスにContentインスタンスを関連付け
        self.space.content.set([self.content])
        self.space.save()

    @pytest.mark.django_db
    def test_space_serializer(self):
        assert self.space
        assert self.space.name == "Test Space"
        assert self.space.name != "Test Spac"

    @pytest.mark.django_db
    def test_space_serializer_with_content(self):
        serializer = SpaceSerializer(self.space)
        assert serializer.data == {
            "id": self.space.id,
            "content": [
                {
                    "id": self.content.id,
                    "model": None,
                    "title": "Test Content",
                    "created_at": self.content.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "updated_at": self.content.updated_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "published_at": self.content.published_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "status": self.content.status.id,
                }
            ],
        }

    @pytest.mark.django_db
    def test_zero_in_name(self):
        """nameにdjango.model.charfieldが拒否する文字列を入れた場合のテスト"""
        serializer = SpaceSerializer(data={"name": "0"})
        serializer.is_valid()
        assert serializer.errors
