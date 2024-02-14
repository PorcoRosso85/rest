from django.test import TestCase
from rest_framework.response import Response

from app.models import Content, Space, Status
from app.serializer import SpaceSerializer


def space_detail(request, pk):
    # status = Status.objects.create(name="Test Status")
    # content = Content.objects.create(title="Test Content", status=status)
    space = Space.objects.get(pk=pk)
    # space.content.set([content])
    # space.save()

    serializer = SpaceSerializer(space)
    return Response(serializer.data)


# space_detailのpytest
class TestSpaceDetailView(TestCase):
    def setUp(self):
        self.space = Space.objects.create(name="Test Space")
        self.status = Status.objects.create(status="draft")
        self.content = Content.objects.create(title="Test Content", status=self.status)
        self.space.content.set([self.content])
        self.space.save()

    def test_space_detail(self):
        response = space_detail(None, self.space.id)
        assert response.data == {
            "id": self.space.id,
            "content": [
                {
                    "id": self.content.id,
                    "model": None,
                    "title": "Test Content",
                    "created_at": self.content.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "updated_at": self.content.updated_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "published_at": self.content.published_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "status": self.content.status.id,
                }
            ],
        }
