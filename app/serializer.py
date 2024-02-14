import pytest
from django.test import TestCase
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail

from app.models import Content, Space, Status


class ResponseSerializer(serializers.Serializer):
    """
    offset: 結果のオフセット <- クエリパラメータ offset
    limit: 結果の制限 <- クエリパラメータ limit
    total: SpaceSerializer
    data: SpaceSerializer, []
    """

    class Meta:
        model = ""
        fields = ["total", "offset", "limit"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["query_params"] = self.context["request"].query_params.get("q")
        return data


class ContentSerializer(serializers.ModelSerializer):
    """
    dataを返すシリアライザ

    @example
    ```json
    "data": [
      {
        "_id": "1234567890",
        "_model": "news",
        "_title": "Hello World",
        "_created_at": "2023-01-23T04:50:00Z",
        "_updated_at": "2023-01-23T04:50:00Z",
        "_published_at": "2023-01-23T04:50:00Z",
        "_status": "published",

        "flexibletext_field": "<div><h2>abcedf</h2><p>abcedf</p><ul><li>abcedf</li></ul></div>",
        "singleline_field": "foobar",
        "multiline_field": "foo\nbar",
        "boolean_field": true,
        "singleselect_field": "value1",
        "datetime_field": "2023-01-23T04:50:00Z",
        "media_field": {
          "url": "https://cms-assets.nilto.com/spaces/1234567890/media/2345678901/_/abc.png",
          "alt": "alternative text"
        },
        "repeat_field": [
          {
            "singleline_field": "foobar",
            "boolean_field": true
          },
          {
            "singleline_field": "foobarbaz",
            "boolean_field": false
          }
        ],
        "combination_field": [
          {
            "luid": "block_a",
            "fields": {
              "multiline_field": "foo\nbar",
              "boolean_field": true
            }
          },
          {
            "luid": "block_b",
            "fields": {
              "datetime_field": "2023-01-23T04:50:00Z",
              "repeat_field": [
                {
                  "singleline_field": "foobar"
                },
                {
                  "singleline_field": "foobarbaz"
                }
              ]
            }
          },
          {
            "luid": "block_a",
            "fields": {
              "multiline_field": "foo\nbar\nbaz",
              "boolean_field": false
            }
          }
        ],
        "reference_field": {
          "_id": "1234567890",
          "_title": "Hello World2",
          "_created_at": "2023-01-23T04:50:00Z",
          "_updated_at": "2023-01-23T04:50:00Z",
          "_published_at": "2023-01-23T04:50:00Z",
          "_status": "draft",
          "reference_field": "2345678901"
        },
        "block1": {
          "singleline_field": "foobar",
          "boolean_field": true
        },
        "block2": {
          "multiline_field": "foo\nbar",
          "datetime_field": "2023-01-23T04:50:00Z"
        }
      }
    ]
    """

    class Meta:
        model = Content
        fields = "__all__"


@pytest.mark.django_db
def test_content_serializer():
    # Statusインスタンスを作成
    status = Status.objects.create(status="draft")

    # Contentインスタンスを作成
    content = Content.objects.create(title="Test Content", status=status)

    # Serializerを作成
    serializer = ContentSerializer(content)

    # Serializerのデータが期待通りであることを確認
    assert serializer.data == {
        "id": content.id,
        "model": None,
        "title": "Test Content",
        "created_at": content.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": content.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "published_at": content.published_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "status": status.id,
    }


class SpaceSerializer(serializers.ModelSerializer):
    """
    total, dataのみを返すシリアライザ
    total: 結果の総数 <- len(data[])
    data: 以下のjsonの[]

    @example
    ```json
    {
      "total;": 34,
      "offset": 20,
      "limit": 10,
    }
    ```
    """

    content = ContentSerializer(read_only=True, many=True)

    class Meta:
        model = Space
        fields = "id", "content"

    def validate(self, data):
        if "content" not in data or not data["content"]:
            raise serializers.ValidationError("content is required")
        return data


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
    def test_space_serializer_with_content_error01(self):
        serializer = SpaceSerializer(self.space)

        # Serializerのデータが期待通りであることを確認
        assert serializer.data != {
            "id": self.space.id,
            "name": "Test Space",
            "associate": self.space.associate,
            "created_at": self.space.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": self.space.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "content": [
                {
                    "id": self.content.id,
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
    def test_space_serializer_with_content_error02(self):
        serializer = SpaceSerializer(self.space)
        assert serializer.data != {
            "id": self.space.id,
            "name": "Test Space",
            "associate": self.space.associate,
            "created_at": self.space.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": self.space.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "content": {
                "id": self.content.id,
                "title": "Test Content",
                "created_at": self.content.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": self.content.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "published_at": self.content.published_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "status": self.content.status.id,
            },
        }

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


class StatusSerializer(serializers.ModelSerializer):
    """
    statusを返すシリアライザ
    """

    class Meta:
        model = Status
        fields = ["status"]

    def validate(self, data):
        if data["status"] == "":
            raise serializers.ValidationError("status is required")
        return data


class TestStatusSerializerPytest:
    """
    statusを返すシリアライザのテスト
    """

    # def setup_method(self):
    #     self.status = Status.objects.create(status="draft")

    @pytest.mark.django_db
    def test_status_serializer_draft(self):
        self.status = Status.objects.create(status="draft")
        assert self.status
        assert self.status.status == "draft"
        serializer = StatusSerializer(data={"status": "draft"})
        serializer.is_valid()

    @pytest.mark.django_db
    def test_status_serializer_none(self):
        self.status = Status.objects.create(status="")
        assert self.status.status == ""
        serializer = StatusSerializer(data={"status": ""})
        serializer.is_valid()
        # is_valid()で期待するエラーであることを確認したい、エラー理由は"status is required"
        assert serializer.errors == {
            "status": [
                ErrorDetail(string='"" is not a valid choice.', code="invalid_choice")
            ]
        }
        assert serializer.data == {"status": ""}


class TestStatusSerializerDjangoTest(TestCase):
    """
    statusを返すシリアライザのテスト
    """

    def test_status_serializer_draft(self):
        self.status = Status.objects.create(status="draft")
        assert self.status.status == "draft"

    def test_status_serializer_review(self):
        self.status = Status.objects.create(status="draft")
        assert self.status.status != "review"

    def test_status_serializer_none(self):
        """nullでも機能してしまうこと＝シリアライザ側でのバリデーションが必要であることを確認するテスト"""
        self.status = Status.objects.create(status="")
        assert self.status.status == ""


from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase


class TestSpaceSerializerHypothesis(HypothesisTestCase):
    # Spaceオブジェクトが存在しない場合のテスト
    def test_no_space(self):
        serializer = SpaceSerializer(data={})
        assert not serializer.is_valid()


#     # Spaceオブジェクトが存在するが、関連するContentオブジェクトが存在しない場合のテスト
#     @given(from_model(Space))
#     def test_space_no_content(self, space):
#         serializer = SpaceSerializer(data={"space": space.id})
#         assert serializer.is_valid()

#     # SpaceとContentの両方が存在するが、Contentが複数ある場合のテスト
#     @given(
#         from_model(Space),
#         from_model(Content, space=from_model(Space)),
#         from_model(Content, space=from_model(Space)),
#     )
#     def test_space_multiple_content(self, space, content1, content2):
#         serializer = SpaceSerializer(
#             data={"space": space.id, "content": [content1.id, content2.id]}
#         )
#         assert serializer.is_valid()

#     # SpaceとContentの両方が存在し、Contentが異なるStatusを持つ場合のテスト
#     @given(
#         from_model(Space),
#         from_model(Content, space=from_model(Space), status="draft"),
#         from_model(Content, space=from_model(Space), status="published"),
#     )
#     def test_space_content_different_status(self, space, content1, content2):
#         serializer = SpaceSerializer(
#             data={"space": space.id, "content": [content1.id, content2.id]}
#         )
#         assert serializer.is_valid()


def gcd(n, m):
    """Compute the GCD of two integers by Euclid's algorithm."""

    n, m = abs(n), abs(m)
    n, m = max(n, m), min(n, m)

    if not n:
        return m

    while m % n != 0:
        n, m = m % n, n
    return n


@given(
    st.integers(min_value=1, max_value=100), st.integers(min_value=500, max_value=500)
)
def test_gcd(n, m):
    d = gcd(n, m)

    assert d > 0
    assert n % d == 0
    assert m % d == 0

    for i in range(d + 1, min(n, m)):
        assert (n % i) or (m % i)


@given(st.integers())
def test_int_str_roundtripping(x):
    assert int(str(x)) == x
