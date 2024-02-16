import pytest

from app.serializer import (
    DataSerializer,
    PublishmentStatusSerializer,
    StructureSerializer,
)
from app.utils import logger


class TestPublishmentStatusSerializer:
    @pytest.mark.django_db
    def test_validate(self):
        data = {"status": "published"}
        logger.info(data)
        serializer = PublishmentStatusSerializer(data=data)
        assert serializer.is_valid() == True

    def test_validate_error(self):
        data = {"status": ""}
        serializer = PublishmentStatusSerializer(data=data)
        assert serializer.is_valid() == False
        assert serializer.errors


class TestDataSerializer:
    @pytest.mark.django_db
    def test_正常(self):
        data = {
            "title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
            "publishmentstatus": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serialized_data = serializer.data
        assert serialized_data["title"] == "title"
        assert serialized_data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": True}
        }

    @pytest.mark.django_db
    def test_正常_Jsonが空でも(self):
        data = {
            "title": "title",
            "value": "",
            "publishmentstatus": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid() == True
        serialized_data = serializer.data
        assert serialized_data["title"] == "title"
        assert serialized_data["value"] == ""

    @pytest.mark.django_db
    def test_正常_Jsonの値が不正確でも(self):
        data = {
            "title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": ""}},
            "publishmentstatus": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid() == True
        serialized_data = serializer.data
        assert serialized_data["title"] == "title"
        assert serialized_data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": ""}
        }

    @pytest.mark.django_db
    def test_正常_publishmentstatusを含む(self):
        data = {
            "title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
            "publishmentstatus": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        data = serializer.data
        logger.debug(f"### data: {data}")
        assert data["title"] == "title"
        assert data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": True}
        }
        assert data["publishmentstatus"][0]["status"] == "draft"


class TestStructureSerializer:
    @pytest.mark.django_db
    def test_正常(self):
        data = {
            "name": "name",
            "description": "description",
        }
        serializer = StructureSerializer(data=data)
        assert serializer.is_valid() == True
        assert serializer.errors == {}


# class TestSpaceSerializer:
#     @pytest.mark.django_db
#     def test_正常(self):
#         data = {
#             "name": "name",
#         }
#         serializer = SpaceSerializer(data=data)
#         assert serializer.is_valid() == True
#         assert serializer.errors == {}