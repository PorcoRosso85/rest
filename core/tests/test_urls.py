import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import Membership, Organization, Space, User
from app.utils import logger


class TestOrganizationView:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        print("\n### SETUP")
        self.organization_instance = Organization.objects.create(name="test org")
        self.user_instance = User.objects.create(name="test user")
        self.space_instance = Space.objects.create(
            name="test space", organization=self.organization_instance
        )

        self.client = APIClient()

        yield (
            self.organization_instance,
            self.user_instance,
            self.space_instance,
            self.client,
        )

        print("\n### TEARDOWN")
        if Organization.objects.count() > 0:
            Organization.objects.all().delete()
        assert Organization.objects.count() == 0
        if User.objects.count() > 0:
            User.objects.all().delete()
        assert User.objects.count() == 0
        if Space.objects.count() > 0:
            Space.objects.all().delete()
        assert Space.objects.count() == 0
        if Membership.objects.count() > 0:
            Membership.objects.all().delete()
        assert Membership.objects.count() == 0

        if self.client:
            self.client = None
        assert self.client is None

    @pytest.mark.django_db
    def test_OrganizationテストインスタンスがOrganization各メソッドで使用される(self):
        pass

    @pytest.mark.django_db
    def test200_組織を作成しレスポンスできる(self):
        response = self.client.post(
            reverse("organization-list"), data={"name": "new org"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new org"

    @pytest.mark.django_db
    def test200_作成したユーザーとオーナーが一致する(self):
        self.organization_instance.create(user=self.user_instance)
        membership = self.organization_instance.membership.first()
        logger.debug(f"### membership: {membership}")
        assert membership is not None
        assert membership.user == self.user_instance

    @pytest.mark.django_db
    def test400_ユーザーが存在するが取得できない(self):
        pass

    @pytest.mark.django_db
    def test200_組織一覧を取得できる(self):
        response = self.client.get(reverse("organization-list"))
        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.skip("組織が存在しない場合のテストを実装する")
    @pytest.mark.django_db
    def test200_組織が存在しない(self):
        self.organization_instance.delete()
        response = self.client.get(reverse("organization-list"))
        assert response.status_code == 200
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test200_組織情報を取得できる(self):
        response = self.client.get(
            reverse("organization-detail", kwargs={"pk": self.organization_instance.id})
        )
        assert response.status_code == 200
        assert response.data["name"] == "test org"

    @pytest.mark.django_db
    def test400_組織情報が取得できていない(self):
        pass

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "data, expected_data_name",
        [
            ({"name": "new org"}, "new org"),
            ({"name": "another org"}, "another org"),
        ],
    )
    def test_正常系_組織を更新できる(self, data, expected_data_name):
        org_id = self.organization_instance.id
        logger.debug(f"### data: {data}")
        response = self.client.put(
            reverse("organization-detail", kwargs={"pk": org_id}),
            data=data,
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == expected_data_name

    @pytest.mark.django_db
    def test異常_ユーザーIDが提供されていないレスポンスエラー(self):
        pass

    @pytest.mark.django_db
    def test200_組織に属するスペースの一覧が取得できる(self):
        response = self.client.get(
            reverse(
                "organization-space-list", kwargs={"pk": self.organization_instance.id}
            ),
        )
        assert response.status_code == 200
        assert len(response.data) > 0
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test200_組織名を更新できる(self):
        response = self.client.put(
            reverse(
                "organization-detail", kwargs={"pk": self.organization_instance.id}
            ),
            data={"name": "new org name"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == "new org name"

    @pytest.mark.django_db
    def test400_組織オーナーを更新できない(self):
        logger.debug("ネストされたManyToManyFieldの更新はできない")
        response = self.client.put(
            reverse(
                "organization-detail", kwargs={"pk": self.organization_instance.id}
            ),
            data={"membership": self.user_instance.id},
            format="json",
        )
        assert response.status_code != 200
        # assert response.data["membership"] == self.user_instance.id

    @pytest.mark.django_db
    def test200_組織オーナーを更新できる(self):
        self.organization_instance.create(user=self.user_instance)
        existing_owner = self.organization_instance.membership.first()
        assert existing_owner is not None
        assert existing_owner.role == "owner"

        # update owner to new_user
        new_user = User.objects.create(name="new user")
        response = self.client.put(
            reverse(
                "organization-update-owner",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id},
            format="json",
        )
        assert response.status_code == 200

        # 既存ユーザーのロールが変更されている
        existing_owner = self.organization_instance.membership.filter(
            user=self.user_instance
        ).first()
        assert existing_owner is not None
        assert existing_owner.role == "member"
        new_owner = self.organization_instance.membership.filter(user=new_user).first()
        assert new_owner is not None
        assert new_owner.role == "owner"

    @pytest.mark.django_db
    def test200_組織メンバーの追加ができる(self):
        new_user = User.objects.create(name="new user")
        role = "member"
        response = self.client.post(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id, "role": role},
            format="json",
        )
        assert response.status_code == 201
        memberships = response.data["membership"]
        for membership in memberships:
            if membership["user"] == new_user.id:
                assert membership["role"] == role

    @pytest.mark.django_db
    def test200_組織メンバーの一覧を取得できる(self):
        new_user = User.objects.create(name="new user")
        role = "member"
        response = self.client.post(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id, "role": role},
            format="json",
        )
        assert response.status_code == 201

        response = self.client.get(
            reverse(
                "organization-memberships",
                kwargs={"pk": self.organization_instance.id},
            ),
        )
        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.django_db
    def test200_組織メンバーの削除ができる(self):
        new_user = User.objects.create(name="new user")
        role = "member"
        response = self.client.post(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id, "role": role},
            format="json",
        )
        assert response.status_code == 201

        response = self.client.get(
            reverse(
                "organization-memberships",
                kwargs={"pk": self.organization_instance.id},
            ),
        )
        assert response.status_code == 200
        assert len(response.data) > 0

        response = self.client.delete(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id},
            format="json",
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test400_組織メンバーの削除ができない(self):
        response = self.client.delete(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": 9999},
            format="json",
        )
        assert response.status_code == 404
        assert "User not found" in response.data["error"]
        assert "User not found" in response.content.decode("utf-8")

    @pytest.mark.django_db
    def test200_組織メンバーを更新できる(self):
        old_user = User.objects.create(name="old user")
        old_user_role = "member"
        response = self.client.post(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": old_user.id, "role": old_user_role},
            format="json",
        )
        assert response.status_code == 201

        response = self.client.get(
            reverse(
                "organization-memberships",
                kwargs={"pk": self.organization_instance.id},
            ),
        )
        assert response.status_code == 200
        assert len(response.data) > 0
        assert len(response.data) == 1
        assert response.data[0]["role"] == old_user_role

        new_user_role = "admin"
        response = self.client.put(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": old_user.id, "role": new_user_role},
            format="json",
        )
        assert response.status_code == 200
        memberships = response.data["membership"]
        for membership in memberships:
            if membership["user"] == old_user.id:
                assert membership["role"] == new_user_role

    @pytest.mark.skip(
        "クライアントからのアップロードができていないためテストをスキップ"
    )
    @pytest.mark.django_db
    def test200_組織アイコンをアップロードできる(self):
        icon_name = f"icon_{uuid.uuid4()}.png"
        file = SimpleUploadedFile(icon_name, b"file_content", content_type="image/png")
        assert file.name == icon_name
        assert file.content_type == "image/png"

        response = self.client.post(
            reverse(
                "organization-icon",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"icon": file},
            format="multipart",
        )
        assert response.status_code == 200

        response = self.client.put(
            reverse(
                "organization-detail", kwargs={"pk": self.organization_instance.id}
            ),
            data={"icon": file},
            format="multipart",
        )
        assert response.status_code == 200

    # []fixme
    @pytest.mark.skip(
        "テストのOrgインスタンスとモデル上のself.organization_instanceが異なるためテストをスキップ"
    )
    @pytest.mark.django_db
    def test200_オーナーが組織を削除できる(self):
        response = self.client.delete(
            reverse(
                "organization-detail",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": self.user_instance.id},
            format="json",
        )
        assert response.status_code == 204

    @pytest.mark.django_db
    def test400_オーナー以外のユーザーが組織削除を試行した場合のエラーハンドリングが適切である(
        self,
    ):
        pass


class TestUserView:
    def setup_method(self, method):
        print("\n### SETUP")
        self.organization_instance = None
        self.user_instance = None
        self.organization_instance = Organization.objects.create(name="test org")
        self.user_instance = User.objects.create(name="test user")
        self.space_instance = Space.objects.create(
            name="test space", organization=self.organization_instance
        )

        self.client = APIClient()

    def teardown_method(self, method):
        print("\n### TEARDOWN")
        if self.organization_instance:
            # self.organization.delete()
            Organization.objects.all().delete()
        if self.user_instance:
            # self.user.delete()
            User.objects.all().delete()
        assert Organization.objects.count() == 0
        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test200_ユーザー一覧を取得できる(self):
        response = self.client.get(reverse("user-list"))
        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.django_db
    def test正常_ユーザーを作成できる(self):
        response = self.client.post(
            reverse("user-list"), data={"name": "new username"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new username"

    @pytest.mark.django_db
    def test200_ユーザーが存在しない(self):
        self.user_instance.delete()
        response = self.client.get(reverse("user-list"))
        assert response.status_code == 200
        assert len(response.data) == 0
