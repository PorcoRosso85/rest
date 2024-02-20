from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import Access, ApiKeys
from app.serializer import AccessSerializer, ApiKeysSerializer

# Create your views here.


def home(request):
    pass


def login_view(request):
    pass


def logout_view(request):
    pass


def serve_asset(request):
    """
    - apikey
    """
    pass


def serve_image(request):
    pass


def collect_data(request):
    pass


def language_choice(request):
    pass


def organization_list(request):
    pass


def organization_detail(request):
    pass


def space_list(request):
    pass


def space_detail(request):
    pass


def content_list(request):
    pass


def content_detail(request):
    pass


def announcements(request):
    pass


class ApiViewSet(ModelViewSet):
    queryset = ApiKeys.objects.all()
    serializer_class = ApiKeysSerializer


import pytest
from rest_framework.test import APIClient

from app.utils import logger


@pytest.mark.django_db
class TestApiViewSet:
    def setup_method(self):
        self.apikey = ApiKeys.objects.create()
        assert self.apikey.id is not None
        self.client = APIClient()

    def test_get_all_apikeys(self):
        response: Response = self.client.get("/apikeys/")
        assert response.status_code == 200

    def test_get_single_apikey(self):
        logger.debug(f"### self.apikey.id: {self.apikey.id}")
        response: Response = self.client.get(f"/apikeys/{self.apikey.id}/")
        logger.debug(f"### response: {response.content}")
        assert response.status_code == 200

    def test_create_apikey(self):
        access = Access.objects.create()  # Accessモデルのインスタンスを作成
        # access field is required
        # data = {
        #     "access": access.id,
        # }
        access_serializer = AccessSerializer(access)
        # []check ネストされたシリアライザの書き込みは非サポート
        data = {
            "access": [
                access_serializer.data,
            ]
        }
        response: Response = self.client.post("/apikeys/", data=data, format="json")
        logger.debug(f"### response: {response.content}")
        assert response.status_code == 201
