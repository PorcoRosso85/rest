import re
from typing import Any, Dict, TypeAlias

from rest_framework import serializers

from app.models import Data, PublishmentStatus, Space, Structure

AttrsType: TypeAlias = Dict[str, Any]


class PublishmentStatusSerializer(serializers.ModelSerializer):
    """
    statusを返すシリアライザ
    """

    class Meta:
        model = PublishmentStatus
        fields = ["status"]

    # []型
    def validate(self, attrs: AttrsType) -> AttrsType:
        if attrs["status"] == "":
            raise serializers.ValidationError("status is required")
        return attrs


class DataSerializer(serializers.ModelSerializer):
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

    # PublishmentStatusモデル側で外部キーを指定しているため、many=Trueを指定する
    publishmentstatus = PublishmentStatusSerializer(many=True)

    class Meta:
        model = Data
        fields = "__all__"


class StructureSerializer(serializers.ModelSerializer):
    """structureを返すシリアライザ"""

    _data = DataSerializer(many=True)

    class Meta:
        model = Structure
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

    data_serializer = DataSerializer(many=True)

    class Meta:
        model = Space
        fields = "id", "content"

    def validate(self, attrs: AttrsType) -> AttrsType:
        if "content" not in attrs or not attrs["content"]:
            raise serializers.ValidationError("content is required")
        # django.model.charfieldが許容できない文字列を拒否する
        if re.match(r"^\d+$", attrs["name"]):
            raise serializers.ValidationError("name is invalid")
        return attrs


# class PlanSerializer(serializers.ModelSerializer):
#     """
#     planを返すシリアライザ
#     """

#     class Meta:
#         model = Plan
#         fields = "__all__"

#     def validate(self, data):
#         # free, standard, premiumのいずれかでない場合はエラー
#         if data["name"] not in ["free", "standard", "premium"]:
#             raise serializers.ValidationError("plan is invalid")
#         return data


# class UserSerializer(serializers.ModelSerializer):
#     """
#     userを返すシリアライザ
#     """

#     class Meta:
#         model = User
#         fields = "__all__"


# class UsageSerializer(serializers.ModelSerializer):
#     """
#     usageを返すシリアライザ
#     """

#     class Meta:
#         model = Usage
#         fields = "__all__"


# class AssociateSerializer(serializers.ModelSerializer):
#     """
#     associateを返すシリアライザ
#     """

#     class Meta:
#         model = Associate
#         fields = "__all__"
