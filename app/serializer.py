import re
from typing import Any, Dict, TypeAlias

import pytest
from rest_framework import serializers

from app.models import (
    Access,
    ApiKeys,
    Data,
    Membership,
    Organization,
    PublishmentStatus,
    Space,
    User,
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

    access = AccessSerializer(many=True, read_only=True)

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


class MembershipSerializer(serializers.ModelSerializer):
    """membershipを返すシリアライザ"""

    class Meta:
        model = Membership
        fields = ["user", "organization", "role", "created_at", "updated_at"]


class OrganizationSerializer(serializers.ModelSerializer):
    """organizationを返すシリアライザ"""

    membership = MembershipSerializer(many=True, read_only=True)
    icon = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "icon",
            "created_at",
            "updated_at",
            "plan",
            "plan_created_at",
            "plan_updated_at",
            "membership",
        ]


from django.core.files.uploadedfile import SimpleUploadedFile


class TestOrganizationSerializer:
    @pytest.mark.django_db
    def test200_組織シリアライザのインスタンス化(self):
        # シリアライザのインスタンス化テスト:
        # Organization インスタンスを使用して OrganizationSerializer をインスタンス化し、期待通りのフィールドが含まれていることを確認する。
        organization = Organization.objects.create(name="test")
        serializer = OrganizationSerializer(organization)

        expected_fields = [
            "id",
            "name",
            "icon",
            "created_at",
            "updated_at",
            "plan",
            "plan_created_at",
            "plan_updated_at",
            "membership",
        ]
        assert serializer.data.keys() == set(expected_fields)

    @pytest.mark.django_db
    def test200_組織アイコンがシリアライズされる(self):
        file = SimpleUploadedFile(
            "icon.jpg", b"file_content", content_type="image/jpeg"
        )
        organization = Organization.objects.create(name="test", icon=file)
        serializer = OrganizationSerializer(organization)
        assert "icon" in serializer.data
        assert serializer.data["icon"] == organization.icon.url

    def test200_組織シリアライザのバリデーション(self):
        # データのバリデーションテスト:
        # 不正なデータ（例えば、長すぎる名前や不正なファイル形式のアイコン）をシリアライザに渡し、適切なバリデーションエラーが発生することを確認する。
        invalid_data = {
            "name": "a" * 256,
            "icon": SimpleUploadedFile(
                "icon.txt", b"file_content", content_type="text"
            ),
        }
        serializer = OrganizationSerializer(data=invalid_data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors
        assert "icon" in serializer.errors


class OrganizationSpaceSerializer(serializers.ModelSerializer):
    """organization.idに関連するspaceを返すシリアライザ"""

    class Meta:
        model = Space
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    """userを返すシリアライザ"""

    membership = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["name", "created_at", "updated_at", "membership"]
