import pytest
from inline_snapshot import snapshot

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
            "_title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
            "_status": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serialized_data = serializer.data
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data["_title"] == "title"
        assert serialized_data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": True}
        }

    @pytest.mark.django_db
    def test_正常_Jsonが空でも(self):
        data = {
            "_title": "title",
            "value": "",
            "_status": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid() == True
        serialized_data = serializer.data
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data["_title"] == "title"
        assert serialized_data["value"] == ""

    @pytest.mark.django_db
    def test_正常_Jsonの値が不正確でも(self):
        data = {
            "_title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": ""}},
            "_status": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid() == True
        serialized_data = serializer.data
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data["_title"] == "title"
        assert serialized_data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": ""}
        }

    @pytest.mark.django_db
    def test_正常_publishmentstatusを含む(self):
        data = {
            "_title": "title",
            "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
            "_status": [{"status": "draft"}],
        }
        serializer = DataSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serialized_data = serializer.data
        # logger.debug(f"### data: {data}")
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data["_title"] == "title"
        assert serialized_data["value"] == {
            "block1": {"singleline_field": "foobar", "boolean_field": True}
        }
        assert serialized_data["_status"][0]["status"] == "draft"


class TestStructureSerializer:
    @pytest.mark.django_db
    def test_正常(self):
        data = {
            "name": "name",
            "description": "description",
            "_data": [
                {
                    "_title": "title",
                    "structure": "structure",
                    "_status": [{"status": "draft"}],
                    "value": {
                        "block1": {"singleline_field": "foobar", "boolean_field": True}
                    },
                }
            ],
        }
        serializer = StructureSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serialized_data = serializer.data
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data["name"] == "name"
        assert serialized_data["description"] == "description"
        assert serialized_data["_data"] == snapshot(
            [
                {
                    # _id
                    "_title": "title",
                    # []fixme structure/_modelがない
                    # _created_at
                    # _updated_at
                    # _published_at
                    "_status": [{"status": "draft"}],
                    "value": {
                        "block1": {
                            "singleline_field": "foobar",
                            "boolean_field": True,
                        }
                    },
                }
            ]
        )


# class TestSpaceSerializer:
#     @pytest.mark.django_db
#     def test_正常(self):
#         data = {
#             "name": "name",
#             "structures": [
#                 {
#                     "name": "name",
#                     "description": "description",
#                     "_data": [
#                         {
#                             "_title": "title",
#                             "value": {
#                                 "block1": {
#                                     "singleline_field": "foobar",
#                                     "boolean_field": True,
#                                 }
#                             },
#                             "_status": [{"status": "draft"}],
#                             "structure": "structure",
#                         }
#                     ],
#                 }
#             ],
#         }
#         serializer = SpaceSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["name"] == "name"
#         assert serialized_data["structures"] == [
#             {
#                 "name": "name",
#                 "description": "description",
#                 "_data": [
#                     {
#                         "_title": "title",
#                         "value": {
#                             "block1": {
#                                 "singleline_field": "foobar",
#                                 "boolean_field": True,
#                             }
#                         },
#                         "_status": [{"status": "draft"}],
#                         "structure": "structure",
#                     }
#                 ],
#             }
#         ]
#         logger.debug(f"### serialized_data: {serialized_data}")
