import logging

import pytest
from inline_snapshot import snapshot

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
        assert space.data.get(id=data2.id)._created_at is not None
        assert space.data.get(id=data2.id)._updated_at is not None


class TestDataModel:
    @pytest.mark.django_db
    def test_modelフィールドにはJson形式のデータを保存できる(self):
        data = Data.objects.create(_model={"1": {"2": {"3": [1, 2, 3]}}})
        assert data._model == snapshot({"1": {"2": {"3": [1, 2, 3]}}})

    # []fixme シグナルが発火しないためスキップ
    @pytest.mark.skip("シグナルが発火しないためスキップ")
    @pytest.mark.django_db
    def test_正常系_シグナルが発火する(self):
        _data = Data.objects.create()
        _data.save()

        publishment_status = PublishmentStatus.objects.create(
            _data=_data, status="published"
        )
        publishment_status.save()

        # データベースのアサーション
        _data.refresh_from_db()
        _data = Data.objects.get(id=_data.id)
        assert _data._published_at is not None


class TestMembershipModel:
    @pytest.mark.django_db
    def test_正常_関連するorganizationとuserを取得する(self):
        user = User.objects.create()
        organization = Organization.objects.create()
        membership = Membership.objects.create(user=user, organization=organization)
        assert membership.organization.id == organization.id
        assert membership.user.id == user.id

        user_from_database = User.objects.get(id=user.id)
        organization_from_database = Organization.objects.get(id=organization.id)
        assert user_from_database.membership.first().id == membership.id
        membership_from_database = Membership.objects.get(id=membership.id)
        assert membership_from_database.organization.id == organization.id

    @pytest.mark.skip
    @pytest.mark.django_db
    def test200_組織を作成したユーザーがオーナーとなっている(self):
        user = User.objects.create(name="owneruser")
        organization = Organization.objects.create(name="organization")
        organization.create(user=user)
        assert organization is not None
        assert organization.membership.first().user.id == user.id


class TestUserModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        user = User.objects.create()
        assert user.id is not None

    @pytest.mark.django_db
    def test_正常_関連するorganizationを取得する(self):
        user = User.objects.create(name="testuser")
        organization1 = Organization.objects.create(name="organization1")
        organization2 = Organization.objects.create(name="organization2")
        membership1 = Membership.objects.create(user=user, organization=organization1)
        membership2 = Membership.objects.create(user=user, organization=organization2)

        # userが所属するorganizationを中間テーブルであるMembershipを介して取得
        organizations = Organization.objects.filter(membership__user=user)
        assert organizations.count() == 2
        assert organizations.first().id == organization1.id
        assert organizations.first().name == "organization1"
        assert organizations.last().id == organization2.id
        assert organizations.last().name == "organization2"

        for organization in organizations:
            assert organization in [organization1, organization2]

    @pytest.mark.django_db
    def test_正常_関連するorganizationを取得する02(self):
        user = User.objects.create(name="testuser")
        organization1 = Organization.objects.create(name="organization1")
        organization2 = Organization.objects.create(name="organization2")
        membership1 = Membership.objects.create(user=user, organization=organization1)
        membership2 = Membership.objects.create(user=user, organization=organization2)

        organization_ids = user.membership.values_list("organization_id", flat=True)
        assert organization_ids.count() == 2
        organizations = [
            Organization.objects.get(id=organization_id)
            for organization_id in organization_ids
        ]
        for organization in organizations:
            assert organization in [organization1, organization2]


class TestOrganizationModel:
    def setup_method(self):
        self.user1 = User.objects.create(name="user1")
        self.user2 = User.objects.create(name="user2")
        self.organization = Organization.objects.create()
        self.organization2 = Organization.objects.create()

    @pytest.mark.django_db
    def test200_クエリが成功する場合(self):
        """クエリが成功する場合"""
        assert self.organization.id is not None

    @pytest.mark.django_db
    def test200_組織一覧が取得できる(self):
        assert Organization.objects.all().count() > 1

    @pytest.mark.django_db
    def test_正常_関連するuserを取得する(self):
        membership1 = Membership.objects.create(
            user=self.user1, organization=self.organization
        )
        membership2 = Membership.objects.create(
            user=self.user2, organization=self.organization
        )

        # organizationに所属するuserを中間テーブルであるMembershipを介して取得
        users = User.objects.filter(membership__organization=self.organization)
        assert users.count() == 2
        assert users.first().id == self.user1.id
        assert users.first().name == "user1"
        assert users.last().id == self.user2.id
        assert users.last().name == "user2"

        for user in users:
            assert user in [self.user1, self.user2]

    @pytest.mark.django_db
    def test500_関連するユーザーが存在しない(self):
        pass

    @pytest.mark.django_db
    def test200_関連する組織が存在しない(self):
        """ユーザーは0以上の組織に所属する"""
        pass

    @pytest.mark.django_db
    def test400_オーナーユーザーが存在しない(self):
        """組織は1以上のオーナーユーザーを所属させる"""
        pass

    @pytest.mark.django_db
    def test200_最低1人のオーナーが存在する(self):
        pass

    @pytest.mark.django_db
    def test200_組織を削除できる(self):
        assert self.organization.id is not None
        self.organization.delete()
        assert Organization.objects.filter(id=self.organization.id).count() == 0
