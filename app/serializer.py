from rest_framework import serializers

from app.models import Content, Status


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


class SpaceSerializer:
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

    pass


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
        "content": {
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
      }
    ]
    """

    class Meta:
        model = Content
        fields = "__all__"


import pytest


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
        "title": "Test Content",
        "created_at": content.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": content.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "published_at": content.published_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "status": status.id,
    }
