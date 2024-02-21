import logging

import pytest
from inline_snapshot import snapshot

from app.models import Access, ApiKeys, Data, Organization, Space, User
from app.utils import logger

logger.setLevel(logging.DEBUG)


class TestApiKeysModel:
    @pytest.mark.django_db
    def test_正常系_Keyがユニークである(self):
        key1 = ApiKeys.objects.create()
        key2 = ApiKeys.objects.create()
        assert key1.key != key2.key

    @pytest.mark.django_db
    def test_正常系_Keyが自動生成される(self):
        key = ApiKeys.objects.create()
        assert key.key is not None

    @pytest.mark.django_db
    def test_正常系_関連するorganizationのidを取得する(self):
        space = Space.objects.create()
        apikey = ApiKeys.objects.create(space=space)
        assert apikey.space.id == space.id

    @pytest.mark.django_db
    def test_異常系_関連するorganizationが存在しない場合(self):
        space = Space.objects.create()
        key = ApiKeys.objects.create()
        assert key.space.id != space.id


class TestAccessModel:
    @pytest.mark.django_db
    def test_default_key(self):
        key = ApiKeys.objects.create()
        access = Access.objects.create()
        assert access.api_key.id == key.id

    @pytest.mark.django_db
    def test_generate_new_api_key(self):
        Access.objects.all().delete()
        ApiKeys.objects.all().delete()
        access = Access.objects.create()
        assert access.api_key is not None


class TestSpaceModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        logger.debug("データを削除します")
        Organization.objects.all().delete()
        Space.objects.all().delete()
        User.objects.all().delete()
        Data.objects.all().delete()

    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        space = Space.objects.create()
        assert space.id is not None

    @pytest.mark.django_db
    def test_正常系_関連するDataのidを取得する(self):
        space = Space.objects.create()
        data = Data.objects.create(space=space)
        assert space.data.first().id == data.id

    @pytest.mark.django_db
    def test_正常系_関連するDataを取得する(self):
        space = Space.objects.create()
        data = Data.objects.create(space=space)
        assert space.data.first().id == data.id

    @pytest.mark.django_db
    def test_正常系_関連するDataを追加する(self):
        space = Space.objects.create()
        assert space.data.count() == 0
        data = Data.objects.create(space=space)
        assert space.data.count() == 1
        data2 = Data.objects.create(space=space)
        assert space.data.count() == 2

    @pytest.mark.django_db
    def test_正常系_関連するDataを削除する(self):
        space: Space = Space.objects.create()
        data: Data = Data.objects.create(space=space)
        assert space.data.count() == 1
        data.delete()
        assert space.data.count() == 0

    @pytest.mark.django_db
    def test_正常系_関連するDataを更新する(self):
        space = Space.objects.create()
        data = Data.objects.create(space=space)
        assert space.data.count() == 1
        data2 = Data.objects.create(space=space)
        assert space.data.count() == 2
        assert space.data.first().id == data.id
        assert space.data.last().id == data2.id

        data2._title = "test"
        data2.value = {"test": "test"}
        data2.save()
        assert space.data.count() == 2
        assert space.data.first().id == data.id
        assert space.data.last().id == data2.id

        # data2.idのデータを取得
        assert space.data.get(id=data2.id)._title == "test"
        assert space.data.get(id=data2.id).value == {"test": "test"}


class TestUserModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        user = User.objects.create()
        assert user.id is not None

    @pytest.mark.django_db
    def test_正常系_関連するorganizationを取得する場合(self):
        """関連するorganizationを取得する場合"""
        user = User.objects.create()
        organization = Organization.objects.create()
        user.organization.add(organization)
        assert user.organization.first().id == organization.id

    @pytest.mark.django_db
    def test_正常系_関連するorganizationとspaceとapikeyを取得する場合(self):
        """関連するorganizationとapi_keyを取得する場合
        user[1, 2]が同じorganization[1]に所属している
        """
        user1 = User.objects.create()
        user2 = User.objects.create()
        organization = Organization.objects.create()
        user1.organization.add(organization)
        user2.organization.add(organization)
        space = Space.objects.create(organization=organization)
        apikey = ApiKeys.objects.create(space=space)

        assert (
            user1.organization.first().spaces.first().api_keys.first().id
            == user2.organization.first().spaces.first().api_keys.first().id
        )

    @pytest.mark.django_db
    def test_正常系_関連するorganizationとspaceとapi_keyを取得する場合(self):
        """関連するorganizationとspaceとapi_keyを取得する場合
        user[1, 2]が同じorganization[1]に所属している
        user[3]は異なるorganization[2]に所属している
        """
        user1 = User.objects.create()
        user2 = User.objects.create()
        user3 = User.objects.create()
        organization1 = Organization.objects.create()
        organization2 = Organization.objects.create()
        space1 = Space.objects.create(organization=organization1)
        space2 = Space.objects.create(organization=organization2)
        api_key1 = ApiKeys.objects.create(space=space1)
        api_key2 = ApiKeys.objects.create(space=space2)
        user1.organization.add(organization1)
        user2.organization.add(organization1)
        user3.organization.add(organization2)

        # user1とuser2が同じorganization1に所属していることを検証
        assert (
            user1.organization.first().spaces.first().api_keys.first().id == api_key1.id
        )
        assert (
            user2.organization.first().spaces.first().api_keys.first().id == api_key1.id
        )

        # user3が異なるorganization2に所属していることを検証
        assert user3.organization.first().id == organization2.id
        assert (
            not user3.organization.first().spaces.first().api_keys.first().id
            == api_key1.id
        )
        assert (
            user3.organization.first().spaces.first().api_keys.first().id == api_key2.id
        )


class TestDataModel:
    @pytest.mark.django_db
    def test_modelフィールドにはJson形式のデータを保存できる(self):
        data = Data.objects.create(_model={"1": {"2": {"3": [1, 2, 3]}}})
        assert data._model == snapshot({"1": {"2": {"3": [1, 2, 3]}}})
