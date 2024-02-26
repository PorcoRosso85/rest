import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app.models import Access, ApiKeys, Organization, Space, User
from app.serializer import (
    AccessSerializer,
    ApiKeysSerializer,
    OrganizationSerializer,
    OrganizationSpaceSerializer,
    SpaceSerializer,
    UserSerializer,
)
from app.utils import logger


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


@pytest.mark.skip
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

    # @pytest.mark.skip("Not implemented")
    def test_create_apikey(self):
        access = Access.objects.create()  # Accessモデルのインスタンスを作成
        access_serializer = AccessSerializer(access)
        # []check ネストされたシリアライザの書き込みは非サポート
        data = {
            "access": [
                access_serializer.data,
            ]
        }
        # /apikeys/でApiSerializerを使ってPOSTリクエストを送信、ネストされたAccessSerializerを使ってデータを作成
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


@pytest.mark.skip
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


class OrganizationView(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def update_owner(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        instance.update_owner(user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def add_membership(self, request, *args, **kwargs):
        organization = self.get_object()
        user_id = request.data.get("user_id")
        role = request.data.get("role")
        user = User.objects.get(id=user_id)
        organization.add_membership(user, role)
        serializer = self.get_serializer(organization)
        return Response(serializer.data, status=201)

    def update_membership(self, request, *args, **kwargs):
        organization = self.get_object()
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        role = request.data.get("role")
        organization.update_membership(user, role)
        serializer = self.get_serializer(organization)
        return Response(serializer.data)

    def remove_membership(self, request, *args, **kwargs):
        organization = self.get_object()
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        organization.remove_membership(user)
        serializer = self.get_serializer(organization)
        return Response(serializer.data)


class OrganizationSpaceView(ModelViewSet):
    serializer_class = OrganizationSpaceSerializer

    def get_queryset(self):
        organization_id = self.kwargs["pk"]
        organization = Organization.objects.get(id=organization_id)
        return organization.spaces.all()


class SpaceView(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
