import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_default_user() -> int:
    user = User.objects.first()
    if user:
        return user.id
    new_user = User.objects.create()
    return new_user.id


class Organization(models.Model):
    PLAN_OPTIONS = [
        ("free", "Free"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    icon = models.ImageField(upload_to="icon/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=100, choices=PLAN_OPTIONS, default="free")
    plan_created_at = models.DateTimeField(default=timezone.now)
    plan_updated_at = models.DateTimeField(default=timezone.now)

    def create(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().save(*args, **kwargs)
        if user is not None:
            membership = Membership.objects.filter(user=user, organization=self)
            if not membership.exists():
                Membership.objects.create(user=user, organization=self, role="owner")

    def update_owner(self, user):
        membership = Membership.objects.filter(organization=self, role="owner")
        # assert membership.exists()
        if membership.exists():
            for member in membership:
                member.role = "member"
                member.save()
        Membership.objects.create(user=user, organization=self, role="owner")

    def add_membership(self, user, role):
        Membership.objects.create(user=user, organization=self, role=role)

    def update_membership(self, user, role):
        membership = Membership.objects.filter(user=user, organization=self)
        if membership.exists():
            membership.update(role=role)
        else:
            raise ValueError("membership not found")

    def remove_membership(self, user):
        membership = Membership.objects.filter(user=user, organization=self)
        if membership.exists():
            membership.delete()
        else:
            raise ValueError("membership not found")

    def upload_icon(self, icon):
        self.icon = icon
        self.save()

    def get_icon_url(self):
        return self.icon.url

    def remove_icon(self):
        self.icon.delete()
        # []check ストレージからの削除はおこなうか

    def get_role(self, *args, **kwargs):
        user_id = kwargs.pop("user_id", None)
        assert user_id is not None
        membership = Membership.objects.filter(user_id=user_id, organization=self)
        assert membership.exists()
        assert membership.first().role is not None
        assert membership.first().role in ["owner", "admin", "member"]
        return membership.first().role


class TestOrganizationModel:
    @pytest.fixture
    def org_and_user(self):
        print("\n### SETUP")
        self.organization = Organization.objects.create(name="test organization")
        self.user = User.objects.create(name="test user")

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
    def test200_組織メンバーのロールを取得する(self, org_and_user):
        membership = Membership.objects.create(
            user=self.user, organization=self.organization
        )
        assert self.organization.membership.exists()
        role = self.organization.get_role(user_id=self.user.id)
        assert role == "member"

    @pytest.mark.django_db
    def test200_組織メンバーのロールを更新する(self, org_and_user):
        membership = Membership.objects.create(
            user=self.user, organization=self.organization, role="owner"
        )
        assert self.organization.membership.exists()
        role = self.organization.get_role(user_id=self.user.id)
        assert role == "owner"

        self.organization.update_membership(self.user, "admin")
        role = self.organization.get_role(user_id=self.user.id)
        assert role == "admin"

    @pytest.mark.django_db
    def test200_組織メンバーを追加できる(self, org_and_user):
        self.organization.add_membership(self.user, "member")
        membership = self.organization.membership.filter(user=self.user)
        assert membership.exists()
        assert membership.first().role == "member"

    @pytest.mark.django_db
    def test200_作成可能(self, org_and_user):
        organization = Organization.objects.create(name="test")
        assert organization.id is not None

    @pytest.mark.django_db
    def test200_オーナー変更ができる(self, org_and_user):
        user = User.objects.create(name="test user")
        organization = Organization.objects.create(name="test")
        organization.create(user=user)
        memberships = organization.membership.filter(user=user)
        assert memberships.exists()
        membership = memberships.first()
        assert membership is not None
        assert membership.user == user
        assert membership.role == "owner"

        new_user = User.objects.create(name="new user")
        organization.update_owner(new_user)
        new_membership = organization.membership.filter(user=new_user).first()
        assert new_membership is not None
        assert new_membership.role == "owner"

        old_owner = organization.membership.filter(user=user)
        assert old_owner.exists()
        assert old_owner.first().role == "member"
        assert old_owner.count() == memberships.count()

        # []todo
        # ownerは一人しか存在しない
        # assert organization.membership.role.filter(user=user).count() == 0

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


class Membership(models.Model):
    ROLE_OPTIONS = [("owner", "Owner"), ("admin", "Admin"), ("member", "Member")]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="membership",
        default=get_default_user,  # type: ignore
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="membership"
    )
    role = models.CharField(max_length=100, default="member", choices=ROLE_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_default_organization() -> int:
    organization = Organization.objects.first()
    if organization:
        return organization.id
    new_organization = Organization.objects.create()
    return new_organization.id


class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(
        Organization,
        related_name="spaces",
        on_delete=models.CASCADE,
        default=get_default_organization,  # type: ignore
    )


def get_default_space() -> int:
    space = Space.objects.first()
    if space:
        return space.id
    new_space = Space.objects.create()
    return new_space.id


class ApiKeys(models.Model):
    """発行したAPIキーを管理する"""

    id = models.AutoField(primary_key=True)
    key = models.CharField(
        max_length=100,
        default=uuid.uuid4,  # type: ignore
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space = models.ForeignKey(
        Space,
        related_name="api_keys",
        on_delete=models.CASCADE,
        default=get_default_space,  # type: ignore
    )


def get_default_api_key() -> int:
    api_key = ApiKeys.objects.first()
    if api_key:
        return api_key.id
    new_api_key = ApiKeys.objects.create()
    return new_api_key.id


class Access(models.Model):
    """Organizationの利用状況を管理する"""

    id = models.AutoField(primary_key=True)
    createad_at = models.DateTimeField(auto_now_add=True)
    api_key = models.ForeignKey(
        ApiKeys,
        related_name="access",
        on_delete=models.CASCADE,
        default=get_default_api_key,  # type: ignore
    )


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    _title = models.CharField(max_length=100)
    _created_at = models.DateTimeField(auto_now_add=True)
    _updated_at = models.DateTimeField(auto_now=True)
    _published_at = models.DateTimeField(null=True, blank=True)
    value = models.JSONField(default=dict)  # type: ignore
    _model = models.JSONField(default=dict)  # type: ignore
    space = models.ForeignKey(
        Space,
        related_name="data",
        on_delete=models.CASCADE,
        default=get_default_space,  # type: ignore
    )


def get_default_data() -> int:
    data = Data.objects.first()
    if data:
        return data.id
    new_data = Data.objects.create()
    return new_data.id


class PublishmentStatus(models.Model):
    STATUS_OPTIONS = [
        ("draft", "Draft"),
        ("review", "Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    status = models.CharField(max_length=100, choices=STATUS_OPTIONS, default="draft")
    _data = models.ForeignKey(
        Data,
        related_name="status",
        on_delete=models.CASCADE,
        default=get_default_data,  # type: ignore
    )
    updated_at = models.DateTimeField(auto_now=True)
