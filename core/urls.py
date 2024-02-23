"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, reverse

from app import views
from app.models import Organization, User

urlpatterns = [
    path("admin/", admin.site.urls),
    # 例えば、ホームページへのルーティング
    path("", views.home, name="home"),
    # 認証関連のエンドポイント
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    # 静的ファイルや画像へのルーティングは通常はurls.pyではなく、Djangoの設定で行われます。
    # しかし、カスタムの静的ファイルサービングをしている場合はこうなるかもしれません。
    path("assets/<path:file_path>", views.serve_asset, name="serve_asset"),
    path("img/<path:image_path>", views.serve_image, name="serve_image"),
    # APIエンドポイント
    path("collect/<str:data>/", views.collect_data, name="collect_data"),
    # 言語選択のエンドポイント
    path("languages/", views.language_choice, name="language_choice"),
    # 組織やプロジェクトに関する情報を扱うエンドポイント
    path("organizations/", views.organization_list, name="organization_list"),
    path(
        "organizations/<int:org_id>/",
        views.organization_detail,
        name="organization_detail",
    ),
    # スペースやコンテンツに関するエンドポイント
    path("spaces/", views.space_list, name="space_list"),
    path("spaces/<int:space_id>/", views.space_detail, name="space_detail"),
    path("spaces/<int:space_id>/content/", views.content_list, name="content_list"),
    path(
        "spaces/<int:space_id>/content/<int:content_id>/",
        views.content_detail,
        name="content_detail",
    ),
    # その他のエンドポイント
    path("app/announcements/", views.announcements, name="announcements"),
    # ... その他多くのエンドポイントがここに続く可能性があります ...
    path("apikeys/", views.ApiViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "apikeys/<int:pk>/",
        views.ApiViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("cookie/", views.CookieView.as_view()),
    path(
        "organization/",
        views.OrganizationView.as_view({"get": "list", "post": "create"}),
        name="organization-list",
    ),
    path(
        "organization/<int:pk>/",
        views.OrganizationView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="organization-detail",
    ),
    path(
        "user/",
        views.UserView.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
]

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from app.utils import logger


class TestOrganizationView:
    def setup_method(self):
        self.client = APIClient()
        self.organization_instance = Organization.objects.create(name="test org")

    @pytest.mark.django_db
    def test200_組織を作成できる(self):
        response: Response = self.client.post(
            reverse("organization-list"), data={"name": "new org"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new org"

    @pytest.mark.django_db
    def test_正常系_組織一覧を取得できる(self):
        response: Response = self.client.get(reverse("organization-list"))
        assert response.status_code == 200
        assert len(response.data) > 0

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
        response: Response = self.client.put(
            reverse("organization-detail", kwargs={"pk": org_id}),
            data=data,
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == expected_data_name

    @pytest.mark.django_db
    def test異常_ユーザーIDが提供されていないレスポンスエラー(self):
        pass


class TestUserView:
    def setup_method(self):
        self.client = APIClient()
        self.user_instance = User.objects.create(name="test username")

    @pytest.mark.django_db
    def test200_ユーザー一覧を取得できる(self):
        response: Response = self.client.get(reverse("user-list"))
        assert response.status_code == 200
        assert len(response.data) > 0

    @pytest.mark.django_db
    def test正常_ユーザーを作成できる(self):
        response: Response = self.client.post(
            reverse("user-list"), data={"name": "new username"}, format="json"
        )
        assert response.status_code == 201
        assert response.data["name"] == "new username"

    @pytest.mark.django_db
    def test200_ユーザーが存在しない(self):
        self.user_instance.delete()
        response: Response = self.client.get(reverse("user-list"))
        assert response.status_code == 200
        assert len(response.data) == 0
