import pytest

from app.models import Content, Status, Structure


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


class TestStatusOption:
    @pytest.mark.django_db
    def test_status_draft(self):
        self.status = Status.objects.create(status="draft")
        assert self.status.status == "draft"

    @pytest.mark.django_db
    def test_status_review(self):
        self.status = Status.objects.create(status="draft")
        assert self.status.status != "review"

    @pytest.mark.django_db
    def test_status_none(self):
        """nullでも機能してしまうこと＝シリアライザ側でのバリデーションが必要であることを確認するテスト"""
        self.status = Status.objects.create(status="")
        assert self.status.status == ""


@pytest.fixture
def content():
    status = Status.objects.create(status="draft")
    return Content.objects.create(title="Test Content", status=status)


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
