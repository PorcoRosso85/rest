import logging

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
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
    def test200_組織を削除できる(self):
        assert self.organization.id is not None
        self.organization.delete()
        assert Organization.objects.filter(id=self.organization.id).count() == 0

    @pytest.mark.django_db
    def test200_組織オーナーをメンバーシップから取得できる(self):
        membership = Membership.objects.create(
            user=self.user1, organization=self.organization
        )
        assert self.organization.membership.first().user == self.user1
        assert (
            Organization.objects.get(id=self.organization.id).membership.first().user
            == self.user1
        )

    @pytest.fixture
    def fixture_org(self):
        print("\n### SETUP")
        self.organization = Organization.objects.create(name="test organization")

        yield self.organization

        print("\n### TEST END")
        print("\n### TEARDOWN")
        if Organization.objects.exists():
            Organization.objects.all().delete()
        assert Organization.objects.count() == 0
        print(" no organization")

    @pytest.mark.django_db
    def test200_組織名を変更できる(self, fixture_org):
        self.organization.update_name("new name")
        assert self.organization.name == "new name"

    @pytest.mark.django_db
    def test200_組織プランを変更できる(self, fixture_org):
        self.organization.update_plan("new plan")
        assert self.organization.plan == "new plan"

    @pytest.fixture
    def org_and_user(self):
        print("\n### SETUP")
        self.user = User.objects.create(name="test user")
        self.organization = Organization.objects.create(
            name="test organization", owner=self.user
        )

        yield self.organization, self.user

        print("\n### TEST END")
        print("\n### TEARDOWN")
        if Organization.objects.exists():
            Organization.objects.all().delete()
        assert Organization.objects.count() == 0
        print(" no organization")

        if User.objects.exists():
            User.objects.all().delete()
        assert User.objects.count() == 0
        print(" no user")

        if Membership.objects.exists():
            Membership.objects.all().delete()
        print(" no membership")

    @pytest.mark.django_db
    def test200_組織を作成したユーザーがメンバーとして関連する(self, org_and_user):
        assert self.organization.membership.filter(user=self.user).exists()

    @pytest.mark.django_db
    def test200_組織メンバーのロールを取得する(self, org_and_user):
        new_user = User.objects.create(name="new user")
        membership = Membership.objects.create(
            user=new_user, organization=self.organization
        )
        assert self.organization.membership.exists()
        role, org_id = self.organization.get_role(user_id=new_user.id)
        assert role == "member"
        assert org_id == self.organization.id

    @pytest.mark.django_db
    def test200_組織メンバーのロールを更新する(self, org_and_user):
        assert self.organization.membership.exists()
        role, org_id = self.organization.get_role(user_id=self.user.id)
        assert org_id == self.organization.id
        assert role == "owner"

        self.organization.update_membership(self.user, "admin")
        role, org_id = self.organization.get_role(user_id=self.user.id)
        assert role == "admin"

    @pytest.mark.django_db
    def test200_組織メンバーを追加できる(self, org_and_user):
        new_user = User.objects.create(name="new user")
        self.organization.add_membership(new_user, "member")

        membership = self.organization.membership.filter(user=new_user)
        assert membership.exists()
        assert membership.first().role == "member"

    @pytest.mark.django_db
    def test200_作成可能(self, org_and_user):
        organization = Organization.objects.create(name="test")
        assert organization.id is not None

    @pytest.mark.django_db
    def test200_オーナー変更ができる(self, org_and_user):
        memberships = self.organization.membership.filter(user=self.user)
        assert memberships.exists()
        membership = memberships.first()
        assert membership is not None
        assert membership.user == self.user
        assert membership.role == "owner"

        new_user = User.objects.create(name="new user")
        self.organization.update_owner(new_user)
        new_membership = self.organization.membership.filter(user=new_user).first()
        assert new_membership is not None
        assert new_membership.role == "owner"

        old_owner = self.organization.membership.filter(user=self.user)
        assert old_owner.exists()
        assert old_owner.first().role == "member"
        assert old_owner.count() == memberships.count()

    @pytest.mark.django_db
    def test200_組織アイコンをサーバーに保存および取得ができる(self, org_and_user):
        file = SimpleUploadedFile("icon.png", b"file_content", content_type="image/png")
        organization = Organization.objects.create(name="test", icon=file)

        organization.save()
        assert organization.icon.name == "icon/icon.png"

        # /iconディレクトリにファイルが保存されている
        saved_file = organization.icon.storage.open(organization.icon.name)
        assert saved_file.read() == b"file_content"

        # データベースに保存されているファイル名が一致している
        file_from_db = Organization.objects.get(id=organization.id).icon
        assert file_from_db.name == organization.icon.name

        # ファイルを削除する
        organization.icon.delete()

        # upload_iconメソッドを使用したテスト
        organization = Organization.objects.create(name="test")
        organization.upload_icon(file)

        # /iconディレクトリにファイルが保存されている
        saved_file = organization.icon.storage.open(organization.icon.name)
        assert saved_file.read() == b"file_content"

        # データベースに保存されているファイル名が一致している
        file_from_db = Organization.objects.get(id=organization.id).icon
        assert file_from_db.name == organization.icon.name

        # ファイルを削除する
        organization.icon.delete()

    @pytest.mark.skip(
        "keep_one_ownerでapp_membershipテーブルが関連されない問題が発生する"
    )
    @pytest.mark.django_db
    def test200_オーナーが一人しかいないことをsave前に確認する(self, org_and_user):
        memberships = self.organization.membership.filter(
            organization=self.organization
        )
        assert memberships.count() == 1
        for membership in memberships:
            assert membership.role == "owner"

        new_user = User.objects.create(name="new user")
        self.organization.add_membership(new_user, "owner")
        memberships = self.organization.membership.filter(
            organization=self.organization
        )
        assert memberships.count() == 2
        for membership in memberships:
            assert membership.role == "owner"

    @pytest.fixture
    def fixture_org_user_space(self):
        print("\n### fixture_org_user_space")
        print("\n### SETUP")
        self.user = User.objects.create(name="test user")
        self.organization = Organization.objects.create(
            name="test organization", owner=self.user
        )
        self.space = Space.objects.create(organization=self.organization)

        yield self.organization, self.user, self.space

        print("\n### TEST ENDS")
        print("\n### TEARDOWN")
        if Organization.objects.exists():
            Organization.objects.all().delete()
        assert Organization.objects.count() == 0
        print(" no organization")

        if User.objects.exists():
            User.objects.all().delete()
        assert User.objects.count() == 0
        print(" no user")

        if Space.objects.exists():
            Space.objects.all().delete()
        assert Space.objects.count() == 0
        print(" no space")

    @pytest.mark.django_db
    def test200_組織が削除され関連するスペースも削除される(
        self, fixture_org_user_space
    ):
        """組織が削除されると関連するスペースも削除される
        削除前関連するスペースの存在を確認
        削除後関連するスペースの削除を確認
        """

        org_id = self.organization.id
        assert Space.objects.filter(organization_id=org_id).exists()
        self.organization.delete()

        assert not Space.objects.filter(organization_id=org_id).exists()
        # with pytest.raises(Space.DoesNotExist):
        #     Space.objects.get(organization=self.organization)
