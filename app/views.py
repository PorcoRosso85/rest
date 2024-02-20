from rest_framework.response import Response
from rest_framework.views import APIView
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

    @pytest.mark.skip("Not implemented")
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


class CookieView(APIView):
    def get(self, request) -> Response:
        response = Response({"message": "General cookie set successfully"})
        response.set_cookie(
            "session_id",
            "your_session_id",
            max_age=3600,
            secure=True,
            httponly=True,
            samesite="Strict",
        )
        response.set_cookie(
            "user_settings",
            "your_user_settings",
            max_age=3600,
            secure=True,
            httponly=True,
            samesite="Strict",
        )
        response.set_cookie(
            "tracking_data",
            "your_tracking_data",
            max_age=3600,
            secure=True,
            httponly=True,
            samesite="Strict",
        )
        return response


class TestSetCookieView:
    def setup_method(self):
        self.client = APIClient()
        assert self.client is not None
        assert isinstance(self.client, APIClient)

    # レスポンスをテストしたい
    def test_set_cookie(self):
        response: Response = self.client.get("/cookie/")
        assert response.status_code == 200
        assert response.cookies["session_id"].value == "your_session_id"
        assert response.cookies["user_settings"].value == "your_user_settings"
        assert response.cookies["tracking_data"].value == "your_tracking_data"
        assert response.cookies["session_id"]["max-age"] == 3600
        assert response.cookies["user_settings"]["max-age"] == 3600
        assert response.cookies["tracking_data"]["max-age"] == 3600
        assert response.cookies["session_id"]["secure"] == True
        assert response.cookies["user_settings"]["secure"] == True
        assert response.cookies["tracking_data"]["secure"] == True
        assert response.cookies["session_id"]["httponly"] == True
        assert response.cookies["user_settings"]["httponly"] == True
        assert response.cookies["tracking_data"]["httponly"] == True
        assert response.cookies["session_id"]["samesite"] == "Strict"
        assert response.cookies["user_settings"]["samesite"] == "Strict"
        assert response.cookies["tracking_data"]["samesite"] == "Strict"
