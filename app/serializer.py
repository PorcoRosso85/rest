import re
from typing import Any, Dict, TypeAlias

from rest_framework import serializers

from app.models import Data, PublishmentStatus, Space, Structure

AttrsType: TypeAlias = Dict[str, Any]


class PublishmentStatusSerializer(serializers.ModelSerializer):
    """statusを返すシリアライザ"""

    class Meta:
        model = PublishmentStatus
        fields = ["status"]

    # []型
    def validate(self, attrs: AttrsType) -> AttrsType:
        if attrs["status"] == "":
            raise serializers.ValidationError("status is required")
        return attrs


class DataSerializer(serializers.ModelSerializer):
    """dataを返すシリアライザ"""

    # PublishmentStatusモデル側で外部キーを指定しているため、many=Trueを指定する
    _status = PublishmentStatusSerializer(many=True)

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
    """ """

    structures = StructureSerializer(many=True)

    class Meta:
        model = Space
        fields = ["id", "name", "structures"]

    def validate(self, attrs: AttrsType) -> AttrsType:
        if "name" not in attrs or not attrs["name"]:
            raise serializers.ValidationError("name is required")
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
