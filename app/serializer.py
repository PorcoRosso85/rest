import re
from typing import Any, Dict, TypeAlias

from rest_framework import serializers

from app.models import (
    Access,
    ApiKeys,
    Data,
    PublishmentStatus,
    Space,
)

AttrsType: TypeAlias = Dict[str, Any]


class PublishmentStatusSerializer(serializers.ModelSerializer):
    """statusを返すシリアライザ"""

    class Meta:
        model = PublishmentStatus
        fields = "__all__"

    def validate(self, attrs: AttrsType) -> AttrsType:
        if attrs["status"] == "":
            raise serializers.ValidationError("status is required")
        return attrs


class DataSerializer(serializers.ModelSerializer):
    """dataを返すシリアライザ"""

    status = PublishmentStatusSerializer(many=True)

    class Meta:
        model = Data
        fields = [
            "_title",
            "_created_at",
            "_updated_at",
            "_published_at",
            "value",
            "_model",
            "status",
        ]


class AccessSerializer(serializers.ModelSerializer):
    """accessを返すシリアライザ"""

    class Meta:
        model = Access
        fields = "__all__"


class ApiKeysSerializer(serializers.ModelSerializer):
    """api_keyを返すシリアライザ"""

    access = AccessSerializer(many=True)

    class Meta:
        model = ApiKeys
        fields = "__all__"


class SpaceSerializer(serializers.ModelSerializer):
    """ """

    _data = DataSerializer(many=True)

    class Meta:
        model = Space
        fields = ["name", "_data"]

    def validate(self, attrs: AttrsType) -> AttrsType:
        if "name" not in attrs or not attrs["name"]:
            raise serializers.ValidationError("name is required")
        # django.model.charfieldが許容できない文字列を拒否する
        if re.match(r"^\d+$", attrs["name"]):
            raise serializers.ValidationError("name is invalid")
        return attrs
