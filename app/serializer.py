import re

from rest_framework import serializers

from app.models import Content, Space, Status


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
        # django.model.charfieldが許容できない文字列を拒否する
        if re.match(r"^\d+$", data["name"]):
            raise serializers.ValidationError("name is invalid")
        return data


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
