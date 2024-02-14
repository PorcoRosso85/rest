import pytest
from django.db import models


class Structure(models.Model):
    """userが作成した構造(モデルと呼ばれる)を管理する"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@pytest.fixture
def structure():
    return Structure.objects.create(
        name="Test Structure",
        description="Test Description",
    )


@pytest.mark.django_db
def test_structure(structure):
    assert structure.name == "Test Structure"
    assert structure.description == "Test Description"
    assert structure.created_at
    assert structure.updated_at


class Status(models.Model):
    """
    draft, review, published, archived
    """

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.ForeignKey(
        Structure, related_name="contents", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status, related_name="contents", on_delete=models.CASCADE, default=1
    )


@pytest.fixture
def status_draft():
    return Status.objects.create(status="draft")


@pytest.fixture
def status_review():
    return Status.objects.create(status="review")


@pytest.mark.django_db
def test_status_draft(status_draft):
    assert status_draft.status == "draft"


@pytest.mark.django_db
def test_status_review(status_review):
    assert status_review.status == "review"


@pytest.fixture
def content(status_draft):
    return Content.objects.create(
        title="Test Content",
        status=status_draft,
    )


@pytest.mark.django_db
def test_content(content):
    assert (
        content.title == "Test Content"
    )  # contentのタイトルが"Test Content"であることを確認
    assert content.created_at  # contentが作成日時を持っていることを確認
    assert content.updated_at  # contentが更新日時を持っていることを確認
    assert content.published_at  # contentが公開日時を持っていることを確認
    assert (
        content.status.status == "draft"
    )  # contentのステータスが"draft"であることを確認
    assert (
        content.status.contents.count() == 1
    )  # contentのステータスに関連付けられたcontentの数が1であることを確認
    assert (
        content.status.contents.first() == content
    )  # contentのステータスに関連付けられた最初のcontentがテスト対象のcontentであることを確認
    assert (
        content.status.contents.last() == content
    )  # contentのステータスに関連付けられた最後のcontentがテスト対象のcontentであることを確認


class Plan(models.Model):
    """
    Userのプランを管理する
    'free', 'standard', 'premium'
    """

    PLAN_OPTIONS = [
        ("free", "Free"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    name = models.CharField(max_length=100, choices=PLAN_OPTIONS)


class User(models.Model):
    """
    Userの情報を管理する
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, related_name="users", on_delete=models.CASCADE)


class Associate(models.Model):
    """
    Userの所属先であり
    複数のSpaceを持つことができる
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="associates", on_delete=models.CASCADE)
    content = models.ForeignKey(
        Content, related_name="associates", on_delete=models.CASCADE
    )


class Space(models.Model):
    """
    どのAssosiatesがどのContentを持っているかを管理する
    AssosiatesとContentの中間テーブル
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associate = models.ManyToManyField(
        Associate, related_name="spaces", blank=True, null=True
    )
    content = models.ManyToManyField(
        Content, related_name="spaces", blank=True, null=True
    )
