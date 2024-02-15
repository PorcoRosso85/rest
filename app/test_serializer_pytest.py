import pytest
from django.forms import model_to_dict
from inline_snapshot import snapshot
from rest_framework.exceptions import ErrorDetail

from app.models import Associate, Content, Plan, Space, Status, Usage, User
from app.serializer import (
    ContentSerializer,
    PlanSerializer,
    SpaceSerializer,
    StatusSerializer,
    UsageSerializer,
    UserSerializer,
)
from app.utils import logger


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
        # assert serializer.errors == snapshot(
        #     {
        #         "status": [
        #             ErrorDetail(
        #                 string='"" is not a valid choice.', code="invalid_choice"
        #             )
        #         ]
        #     }
        # )
        assert serializer.data == {"status": ""}


class TestContentSerializer:
    def setup_method(self):
        self.status = Status.objects.create(status="draft")
        self.content = Content.objects.create(title="Test Content", status=self.status)

    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        # Serializerを作成
        serializer = ContentSerializer(self.content)
        serializer_data = dict(serializer.data)
        serializer_data.pop("id", None)
        serializer_data.pop("created_at", None)
        serializer_data.pop("updated_at", None)
        serializer_data.pop("published_at", None)
        serializer_data.pop("status", None)
        assert serializer_data == snapshot(
            {
                # "id": self.content.id,
                "title": "Test Content",
                # "created_at": self.content.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                # "updated_at": self.content.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                # "published_at": self.content.published_at.strftime(
                #     "%Y-%m-%dT%H:%M:%S.%fZ"
                # ),
                "model": None,
                # "status": self.status.id,
            }
        )

    @pytest.mark.django_db
    def test_正常_バリデーション(self):
        serializer = ContentSerializer(
            data={"title": "Test Content", "status": self.status.id}
        )
        serializer.is_valid()
        assert serializer.errors == {}
        assert serializer.is_valid() is True


class TestPlanSerializer:
    # def setup_method(self):
    #     self.plan = Plan.objects.create(name="free")

    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        # Serializerを作成
        serializer = PlanSerializer(data={"name": "free"})
        serializer.is_valid()
        assert serializer.data == {"name": "free"}
        assert serializer.errors == {}
        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_異常_空文字列(self):
        # Serializerを作成
        serializer = PlanSerializer(data={"name": ""})
        serializer.is_valid()
        assert serializer.is_valid() is False
        assert serializer.errors == snapshot(
            {
                "name": [
                    ErrorDetail(
                        string='"" is not a valid choice.', code="invalid_choice"
                    )
                ]
            }
        )
        assert serializer.data == {"name": ""}
        assert serializer.is_valid() is False
        assert serializer.is_valid() == False


class TestUserSerializer:
    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        plan = Plan.objects.create(name="free")
        user = User.objects.create(name="Test User", plan=plan)
        # Serializerを作成
        serializer = UserSerializer(data={"name": "Test User", "plan": plan.id})
        serializer.is_valid()
        assert serializer.is_valid() is True
        assert serializer.data == snapshot({"name": "Test User", "plan": 1})
        assert serializer.errors == snapshot(
            # {
            #     "plan": [
            #         ErrorDetail(
            #             string="Incorrect type. Expected pk value, received str.",
            #             code="incorrect_type",
            #         )
            #     ]
            # }
            {}
        )

    @pytest.mark.django_db
    def test_異常_空文字列(self):
        # Serializerを作成
        serializer = UserSerializer(data={"name": ""})
        serializer.is_valid()
        assert serializer.is_valid() is False
        assert serializer.errors == snapshot(
            {
                "name": [
                    ErrorDetail(string="This field may not be blank.", code="blank")
                ],
                "plan": [
                    ErrorDetail(string="This field is required.", code="required")
                ],
            }
        )
        assert serializer.data == {"name": ""}
        assert serializer.is_valid() is False


class TestUsageSerializer:
    # def setup_method(self):
    #     self.usage = Usage.objects.create(name="Test Usage")

    @pytest.mark.django_db
    def test_異常_空文字列(self):
        # Serializerを作成
        serializer = UsageSerializer(data={"data_transported": "", "api_requested": ""})
        serializer.is_valid()
        assert serializer.errors == snapshot(
            {
                "data_transported": [
                    ErrorDetail(string="A valid integer is required.", code="invalid")
                ],
                "api_requested": [
                    ErrorDetail(string="A valid integer is required.", code="invalid")
                ],
            }
        )
        assert serializer

    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        usage = Usage.objects.create(data_transported=1, api_requested=1)
        # Serializerを作成
        serializer = UsageSerializer(data={"data_transported": 1, "api_requested": 1})
        serializer.is_valid()
        assert serializer.validated_data == {"data_transported": 1, "api_requested": 1}
        assert serializer.errors == {}
        assert serializer.is_valid() is True

        serializer.save()
        # 保存後のデータを確認
        serializer_data = dict(serializer.data)
        serializer_data.pop("id", None)
        serializer_data.pop("createad_at", None)
        assert serializer_data == snapshot(
            {
                # "id": usage.id | usage.id + 1,
                "data_transported": 1,
                "api_requested": 1,
                # "createad_at": usage.createad_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
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
        self.content_serializer = ContentSerializer(
            self.content,
            # read_only=True, many=True
        )
        # SpaceインスタンスにContentインスタンスを関連付け
        self.space.content.set([self.content])
        self.space.save()

    @pytest.mark.django_db
    def test_status(self):
        gotten_status = model_to_dict(self.space.content.all()[0].status)
        gotten_status.pop("id", None)
        assert gotten_status == snapshot(
            {
                # "id": 4,
                "status": "draft"
            }
        )

    @pytest.mark.django_db
    def test_content(self):
        # logger.debug(self.space.content.all()[0])
        logger.debug(model_to_dict(self.space.content.all()[0]))
        gotten_content = model_to_dict(self.space.content.all()[0])
        gotten_content.pop("id", None)
        gotten_content.pop("status", None)
        assert gotten_content == snapshot(
            {
                # "id": 1,
                "model": None,
                "title": "Test Content",
                # "status": 4
            }
        )

    @pytest.mark.django_db
    def test_正常_オブジェクトから(self):
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

    # @pytest.mark.django_db
    # def test_正常_バリデーションから(self):
    #     logger.debug(f"content_serializer.data: {self.content_serializer.data}")
    #     logger.debug(f"content_serializer.data[]: {[self.content_serializer.data]}")
    #     # []fixme: data.contentに入れるものが不明
    #     # シリアライザにオブジェクト完成を渡せば機能するが、バリデーションを機能させられない
    #     serializer = SpaceSerializer(
    #         data={"name": "Test Space", "content": [self.content_serializer.data]}
    #     )
    #     serializer.is_valid()
    #     assert serializer.errors == {}
    #     assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_フィールドが拒否するバリデーションのチェック(self):
        """nameにdjango.model.charfieldが拒否する文字列を入れた場合のテスト"""
        serializer = SpaceSerializer(data={"name": "0"})
        serializer.is_valid()
        assert serializer.errors


class TestAssociateModel:
    def setup_method(self):
        self.plan = Plan.objects.create(name="free")
        self.user = User.objects.create(name="Test User", plan=self.plan)
        self.space = Space.objects.create(name="Test Space")
        self.usage = Usage.objects.create(data_transported=1, api_requested=1)
        self.associate = Associate.objects.create(
            name="Test Associate",
            member=self.user,
            space=self.space,
            usage=self.usage,
        )

    @pytest.mark.django_db
    def test_正常_期待する出力(self):
        assert self.associate
