import pytest
from django.db import models


class Structure(models.Model):
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


class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Key
    structure = models.ForeignKey(
        Structure, related_name="spaces", on_delete=models.CASCADE
    )


@pytest.fixture
def space(structure):
    return Space.objects.create(
        name="Test Space",
        description="Test Description",
        structure=structure,
    )


@pytest.mark.django_db
def test_space(space):
    assert space.name == "Test Space"
    assert space.description == "Test Description"
    assert space.created_at
    assert space.updated_at
    assert space.structure == space.structure
    assert space.structure.name == "Test Structure"
    assert space.structure.description == "Test Description"
    assert space.structure.created_at
    assert space.structure.updated_at
    assert space.structure.spaces.count() == 1
    assert space.structure.spaces.first() == space
    assert space.structure.spaces.last() == space


class Status(models.Model):
    """
    draft, review, published, archived
    """

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)


class Content(models.Model):
    id = models.AutoField(primary_key=True)
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
