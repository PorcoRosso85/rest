import pytest
from inline_snapshot import snapshot

from app.models import Data, Space
from app.serializer import DataSerializer, SpaceSerializer

# class TestPublishmentStatusSerializer:
#     @pytest.mark.django_db
#     def test_validate(self):
#         data = {"status": "published"}
#         serializer = PublishmentStatusSerializer(data=data)
#         assert serializer.is_valid() == True

#     def test_validate_error(self):
#         data = {"status": ""}
#         serializer = PublishmentStatusSerializer(data=data)
#         assert serializer.is_valid() == False
#         assert serializer.errors

#     @pytest.fixture
#     def fixture_PublishmentStatusにデータを登録(self):
#         data = [
#             {
#                 "status": "draft",
#             },
#             {
#                 "status": "review",
#             },
#             {
#                 "status": "published",
#             },
#             {
#                 "status": "archived",
#             },
#         ]

#         serializer_data_list: List[Union[Dict[str, str], List[str]]] = []
#         for d in data:
#             serializer = PublishmentStatusSerializer(data=d)

#             assert serializer.is_valid(), serializer.errors
#             serializer.save() if serializer.is_valid() else ValueError(
#                 serializer.errors
#             )
#             serializer_data: Union[Dict[str, str], List[str]] = serializer.data
#             serializer_data_list.append(serializer_data)

#         return serializer_data_list

#     @pytest.mark.django_db
#     def test_Fixtureのデータが登録されている(
#         self, fixture_PublishmentStatusにデータを登録
#     ):
#         for data in fixture_PublishmentStatusにデータを登録:
#             assert data["status"] in ["draft", "review", "published", "archived"]

#         # データベースのデータを取得
#         result = PublishmentStatus.objects.all()
#         assert len(result) == 4
#         for r in result:
#             assert r.status in ["draft", "review", "published", "archived"]


# class TestDataSerializer:
#     @pytest.mark.django_db
#     def test_正常(self):
#         data = {
#             "_title": "title",
#             "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
#             "_status": [{"status": "draft"}],
#         }
#         serializer = DataSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["_title"] == "title"
#         assert serialized_data["value"] == {
#             "block1": {"singleline_field": "foobar", "boolean_field": True}
#         }

#     @pytest.mark.django_db
#     def test_正常_Jsonが空でも(self):
#         data = {
#             "_title": "title",
#             "value": "",
#             "_status": [{"status": "draft"}],
#         }
#         serializer = DataSerializer(data=data)
#         assert serializer.is_valid() == True
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["_title"] == "title"
#         assert serialized_data["value"] == ""

#     @pytest.mark.django_db
#     def test_正常_Jsonの値が不正確でも(self):
#         data = {
#             "_title": "title",
#             "value": {"block1": {"singleline_field": "foobar", "boolean_field": ""}},
#             "_status": [{"status": "draft"}],
#         }
#         serializer = DataSerializer(data=data)
#         assert serializer.is_valid() == True
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["_title"] == "title"
#         assert serialized_data["value"] == {
#             "block1": {"singleline_field": "foobar", "boolean_field": ""}
#         }

#     @pytest.mark.django_db
#     def test_正常_publishmentstatusを含む(self):
#         data = {
#             "_title": "title",
#             "value": {"block1": {"singleline_field": "foobar", "boolean_field": True}},
#             "_status": [{"status": "draft"}],
#         }
#         serializer = DataSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         # logger.debug(f"### data: {data}")
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["_title"] == "title"
#         assert serialized_data["value"] == {
#             "block1": {"singleline_field": "foobar", "boolean_field": True}
#         }
#         assert serialized_data["_status"][0]["status"] == "draft"

#     # []check このテストはエラーになる
#     # なぜなら、ネストされたPublishmentStatusSerializerがデータベースに登録できないため
#     # 登録するためにはDataSerializerのsaveメソッドをオーバーライドする必要がある
#     # @pytest.fixture
#     # def fixture_複数のDataデータをデータベースに登録する(self):
#     #     data = [
#     #         {
#     #             "_title": "title1",
#     #             "value": {
#     #                 "block1": {"singleline_field": "foobar", "boolean_field": True}
#     #             },
#     #             "_status": [{"status": "draft"}],
#     #         },
#     #         {
#     #             "_title": "title2",
#     #             "value": {
#     #                 "block1": {"singleline_field": "foobar", "boolean_field": True}
#     #             },
#     #             "_status": [{"status": "draft"}],
#     #         },
#     #         {
#     #             "_title": "title3",
#     #             "value": {
#     #                 "block1": {"singleline_field": "foobar", "boolean_field": True}
#     #             },
#     #             "_status": [{"status": "draft"}],
#     #         },
#     #     ]

#     #     serializer_data_list: List[Union[Dict[str, str], List[str]]] = []
#     #     for d in data:
#     #         serializer = DataSerializer(data=d)

#     #         assert serializer.is_valid(), serializer.errors
#     #         serializer.save() if serializer.is_valid() else ValueError(
#     #             serializer.errors
#     #         )
#     #         serializer_data: Union[Dict[str, str], List[str]] = serializer.data
#     #         serializer_data_list.append(serializer_data)

#     #     return serializer_data_list

#     # @pytest.mark.django_db
#     # def test_Fixtureのデータが登録されている(
#     #     self, fixture_複数のDataデータをデータベースに登録する
#     # ):
#     #     # すでにデータベースに登録されているデータをシリアライザで取得
#     #     result = DataSerializer(Data.objects.all(), many=True).data
#     #     assert len(result) == 3
#     #     for r in result:
#     #         assert r["_title"] in ["title1", "title2", "title3"]
#     #         assert r["value"] == {
#     #             "block1": {"singleline_field": "foobar", "boolean_field": True}
#     #         }
#     #         assert r["_status"][0]["status"] == "draft"


# class TestStructureSerializer:
#     @pytest.mark.django_db
#     def test_正常(self):
#         data = {
#             "name": "name",
#             "description": "description",
#             "_data": [
#                 {
#                     "_title": "title",
#                     "structure": "structure",
#                     "_status": [{"status": "draft"}],
#                     "value": {
#                         "block1": {"singleline_field": "foobar", "boolean_field": True}
#                     },
#                 }
#             ],
#         }
#         serializer = StructureSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         assert serialized_data["name"] == "name"
#         assert serialized_data["description"] == "description"
#         assert serialized_data["_data"] == snapshot(
#             [
#                 {
#                     # _id
#                     "_title": "title",
#                     # []fixme structure/_modelがない
#                     # _created_at
#                     # _updated_at
#                     # _published_at
#                     "_status": [{"status": "draft"}],
#                     "value": {
#                         "block1": {
#                             "singleline_field": "foobar",
#                             "boolean_field": True,
#                         }
#                     },
#                 }
#             ]
#         )


# class TestAccessSerializer:
#     @pytest.mark.django_db
#     def test_正常(self):
#         data = {
#             # "api_key": 1,
#         }
#         serializer = AccessSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"
#         # assert serialized_data["api_key"] == "api_key"

#     @pytest.mark.django_db
#     def test_アクセスインスタンスのシリアライズ(self):
#         access = Access.objects.create()
#         serializer = AccessSerializer(access)
#         data = serializer.data
#         assert data["id"] == access.id
#         assert data["api_key"] == access.api_key.id

#     @pytest.mark.django_db
#     def test_不正なデータのエラーハンドリング(self):
#         data = {"api_key": 9999}  # 存在しないAPIキー
#         serializer = AccessSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "api_key" in serializer.errors


# class TestApiKeysSerializer:
#     @pytest.mark.django_db
#     def test_ApiKeysインスタンスのシリアライズ(self):
#         api_key = ApiKeys.objects.create()
#         serializer = ApiKeysSerializer(api_key)
#         data = serializer.data
#         assert data["id"] == api_key.id
#         assert data["api_key"] == str(api_key.api_key)

#     @pytest.mark.django_db
#     def test_不正なデータのエラーハンドリング(self):
#         ApiKeys.objects.create(api_key="test_key")
#         data = {"api_key": "test_key"}  # 重複したキー
#         serializer = ApiKeysSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "api_key" in serializer.errors

#     @pytest.mark.django_db
#     def test_異常_重複したapiKeyの登録(self):
#         api_key = ApiKeys.objects.create()
#         access = Access.objects.create(api_key=api_key)
#         data = {
#             "api_key": str(api_key.api_key),
#             "access": [{"id": access.id}],
#         }
#         serializer = ApiKeysSerializer(data=data)
#         assert not serializer.is_valid(), serializer.errors
#         serialized_data = serializer.data
#         assert isinstance(
#             serialized_data, dict
#         ), f"Expected dict, got {type(serialized_data)}"

#     @pytest.mark.django_db
#     def test_正常系_バリデーションが成功する場合(self):
#         """バリデーションが成功する場合"""
#         api_key = ApiKeys.objects.create()
#         access = Access.objects.create(api_key=api_key)
#         data = {
#             "access": [{"id": access.id}],
#         }
#         serializer = ApiKeysSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors


class TestSpaceSerializer:
    @pytest.mark.django_db
    def test_異常_バリデーションエラー_noname(self):
        """
        異常系
        nameがない
        """
        data = {"_data": []}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    @pytest.mark.django_db
    def test_異常_バリデーションエラー_blankname(self):
        """
        異常系
        nameが空
        """
        data = {"name": "", "_data": []}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    @pytest.mark.django_db
    def test_異常_バリデーションエラー_nodata(self):
        """
        異常系
        dataがない
        """
        data = {"name": "name"}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "_data" in serializer.errors

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_異常_バリデーションエラー_blankdata(self):
        """
        異常系
        dataが空
        """
        # []check dataはblankでもいいのか
        data = {"name": "name", "_data": []}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "_data" in serializer.errors

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_異常_バリデーションエラー_invalidname(self):
        """
        異常系
        nameが不正
        """
        # []check nameが数字でもいいのか
        data = {"name": 123, "_data": []}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    @pytest.mark.django_db
    def test_異常_バリデーションエラー_invaliddata(self):
        """
        異常系
        dataが不正
        """
        # []check dataが数字でもいいのか
        data = {"name": "name", "_data": 123}
        serializer = SpaceSerializer(data=data)
        assert not serializer.is_valid()
        assert "_data" in serializer.errors

    @pytest.mark.django_db
    def test_正常_SpaceシリアライザでSpaceを取得する_複数のDataを持つSpace(self):
        """
        正常系
        space 1 : data N
        """
        # Dataの外部キーのために、Spaceを作成
        # Dataを絞り込みたい場合は、Spaceを作成して、そのSpaceに紐づくDataを作成する
        space_instance = Space.objects.create(name="spacename")

        # Dataシリアライザのために、データを作成
        data_instance = Data.objects.create(
            _title="datatitle",
            value={"block1": {"singleline_field": "foobar", "boolean_field": True}},
            space=space_instance,
        )

        # Spaceシリアライザのために、データを作成
        # _data = DataSerializer()
        request_data = [DataSerializer(data_instance).data]

        data = {"name": "requestname", "_data": request_data}
        serializer = SpaceSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serialized_data = serializer.data
        assert isinstance(
            serialized_data, dict
        ), f"Expected dict, got {type(serialized_data)}"
        assert serialized_data == snapshot(
            {
                "name": "requestname",
                "_data": [
                    # OrderedDict(
                    {
                        "_title": "datatitle",
                        "value": {
                            "block1": {
                                "singleline_field": "foobar",
                                "boolean_field": True,
                            }
                        },
                        "_model": {},
                        "status": [],
                    }
                    # )
                ],
            }
        )

    @pytest.mark.django_db
    def test_正常_Spaceシリアライザでデータを更新する(self):
        space_instance = Space.objects.create(name="name")
        data_instance = Data.objects.create(
            _title="title",
            value={"block1": {"singleline_field": "foobar", "boolean_field": True}},
            space=space_instance,
        )

        updated_space = {
            "name": "updated name",
            "_data": [DataSerializer(data_instance).data],
        }

        space_serializer = SpaceSerializer(
            instance=space_instance, data=updated_space, partial=True
        )

        assert space_serializer.is_valid()

        space_serializer.save()

        updated_space_instance = Space.objects.get(id=space_instance.id)
        assert updated_space_instance.name == "updated name"

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_正常_SpaceシリアライザからDataシリアライザを使ってデータを更新する(self):
        space_instance = Space.objects.create(name="name")
        data_instance = Data.objects.create(
            _title="title",
            value={"block1": {"singleline_field": "foobar", "boolean_field": True}},
            space=space_instance,
        )

        updated_data = {
            "_title": "updated title",
            "value": {
                "block1": {"singleline_field": "updated foobar", "boolean_field": False}
            },
        }

        updated_space = {"name": "updated name", "_data": [updated_data]}

        space_serializer = SpaceSerializer(
            instance=space_instance, data=updated_space, partial=True
        )

        assert space_serializer.is_valid(), space_serializer.errors

        # データの更新
        space_serializer.save()

        # データの確認
        updated_space_instance = Space.objects.get(id=space_instance.id)
        assert updated_space_instance.name == "updated name"
        updated_data_instance = Data.objects.get(id=data_instance.id)

        # []todo SpaceSerializerのsaveメソッドをオーバーライドして、DataSerializerを使ってデータを更新する
        assert updated_data_instance._title == "updated title"
        assert updated_data_instance.value == {
            "block1": {"singleline_field": "updated foobar", "boolean_field": False}
        }


class TestDataSerializer:
    @pytest.mark.django_db
    def test_正常_Dataシリアライザでデータを更新する(self):
        # 初期データの作成
        space_instance = Space.objects.create(name="name")
        data_instance = Data.objects.create(
            _title="title",
            value={"block1": {"singleline_field": "foobar", "boolean_field": True}},
            space=space_instance,
        )

        # 更新データ
        updated_data = {
            "_title": "updated title",
            "value": {
                "block1": {"singleline_field": "updated foobar", "boolean_field": False}
            },
        }

        # シリアライザの初期化
        serializer = DataSerializer(
            instance=data_instance, data=updated_data, partial=True
        )

        # データの検証
        assert serializer.is_valid()

        # データの更新
        serializer.save()

        # データの確認
        updated_data_instance = Data.objects.get(id=data_instance.id)
        assert updated_data_instance._title == "updated title"
        assert updated_data_instance.value == {
            "block1": {"singleline_field": "updated foobar", "boolean_field": False}
        }

    @pytest.mark.django_db
    def test_正常_Dataシリアライザでデータを削除する(self):
        # 初期データの作成
        space = Space.objects.create(name="name")
        data_instance = Data.objects.create(
            _title="title",
            value={"block1": {"singleline_field": "foobar", "boolean_field": True}},
            space=space,
        )

        # データの削除
        data_instance.delete()

        # データの確認
        with pytest.raises(Data.DoesNotExist):
            Data.objects.get(id=data_instance.id)
