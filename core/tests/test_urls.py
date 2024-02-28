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
        self.user_instance = User.objects.create(name="test user")
        self.organization_instance = Organization.objects.create(
            name="test org", owner=self.user_instance
        )
        self.space_instance = Space.objects.create(
            name="test space", organization=self.organization_instance
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_instance)

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
        # []fixme
        assert response.data["id"] == self.organization_instance.id + 1

    @pytest.mark.django_db
    def test200_作成したユーザーとオーナーが一致する(self):
        membership = self.organization_instance.membership.first()
        logger.debug(f"### membership: {membership}")
        assert membership is not None
        assert membership.user == self.user_instance

    @pytest.mark.django_db
    def test200_組織のメンバーシップを取得できる(self):
        response = self.client.get(
            reverse(
                "organization-memberships", kwargs={"pk": self.organization_instance.id}
            )
        )
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.skip("list_membershipsうまく行かない")
    @pytest.mark.django_db
    def test200_組織を作成したユーザーがメンバーシップとして関連している(self):
        response = self.client.get(
            reverse(
                "organization-memberships", kwargs={"pk": self.organization_instance.id}
            )
        )
        assert response.status_code == 200
        assert len(response.data) > 0

        # 組織を作成
        new_user = User.objects.create(name="new user")
        client = APIClient()
        client.force_authenticate(user=new_user)
        response = client.post(
            reverse("organization-list"), data={"name": "new org"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new org"
        # 追加で作成されたから
        assert response.data["id"] == self.organization_instance.id + 1

        response = client.get(
            reverse("organization-memberships", kwargs={"pk": response.data["id"]})
        )
        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.skip("オーナーのチェックは後ほど")
    @pytest.mark.django_db
    def test200_組織を作成したユーザーがオーナーでありメンバーシップとして関連している(
        self,
    ):
        response = self.client.post(
            reverse("organization-list"), data={"name": "new org"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new org"

        # 作成された組織のidの一致を
        # []fixme
        assert response.data["id"] == self.organization_instance.id + 1

        # 組織のメンバーシップの取得
        response = self.client.get(
            reverse("organization-memberships", kwargs={"pk": response.data["id"]})
        )
        assert response.status_code == 200
        assert len(response.data) > 0
        assert response.data[0]["role"] == "owner"

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
        response = self.client.get(
            reverse(
                "organization-memberships",
                kwargs={"pk": self.organization_instance.id},
            ),
        )
        assert response.status_code == 200
        assert response.data[0]["role"] == "owner"
        assert len(response.data) > 0
        assert len(response.data) == 1

        new_user = User.objects.create(name="new user")
        new_user_role = "admin"
        response = self.client.put(
            reverse(
                "organization-update-membership",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": self.user_instance.id, "role": new_user_role},
            format="json",
        )
        assert response.status_code == 200
        memberships = response.data["membership"]
        for membership in memberships:
            if membership["user"] == new_user.id:
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

    @pytest.mark.django_db
    def test200_組織オーナーは組織を削除できる(self):
        print(f"### self.organization_instance.id: {self.organization_instance.id}")
        print("組織インスタンスがモデル上でselfとなっていることを確認した")

        print(f"### self.user_instance.id: {self.user_instance.id}")

        membership = Membership.objects.create(
            user=self.user_instance,
            organization=self.organization_instance,
            role="owner",
        )

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
    def test403_組織オーナー以外のメンバーシップは組織を削除できない(self):
        new_user = User.objects.create(name="new user")
        membership = Membership.objects.create(
            user=new_user,
            organization=self.organization_instance,
        )
        response = self.client.delete(
            reverse(
                "organization-detail",
                # []fixme new_userの組織が見つからない
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"user_id": new_user.id},
            format="json",
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test400_組織オーナーでないメンバーシップは組織情報を変更できない(self):
        """組織オーナーでないメンバーシップは組織情報を変更できない"""
        response = self.client.put(
            reverse(
                "organization-detail",
                kwargs={"pk": self.organization_instance.id},
            ),
            data={"name": "new org name"},
            format="json",
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test200_組織オーナーは組織情報を変更できる(self):
        pass


class TestUserView:
    @pytest.fixture(autouse=True)
    def fixture_setup_teardown(self):
        self.user_instance = User.objects.create(name="test user")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_instance)

        yield self.user_instance, self.client

        if User.objects.count() > 0:
            User.objects.all().delete()
        assert User.objects.count() == 0
        if self.client:
            self.client = None
        assert self.client is None

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

    @pytest.mark.django_db
    def test200_ログインユーザーの情報を取得できる(self):
        response = self.client.get(
            reverse("user-detail", kwargs={"pk": self.user_instance.id})
        )
        assert response.status_code == 200
        assert response.data["name"] == self.user_instance.name

    @pytest.mark.django_db
    def test400_ログインユーザー以外のユーザーが情報を取得できない(self):
        self.client.force_authenticate(user=None)

        new_user = User.objects.create(name="new user")
        response = self.client.get(reverse("user-detail", kwargs={"pk": new_user.id}))
        assert response.status_code == 403
        # assert "Forbidden" in response.data["detail"]
        assert "Authentication" in response.data["detail"]
        # assert "Forbidden" in response.content.decode("utf-8")
