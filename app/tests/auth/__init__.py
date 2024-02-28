test_design_for_auth = {
    "認証・認可": {
        "項目": [
            {
                "トークンベース認証動作確認": [
                    "正常系_トークンが発行される",
                    "正常系_トークンが正しい",
                    "異常系_トークンが発行されない",
                    "異常系_エラーレスポンスが返却される",
                ]
            },
            {
                "適切なユーザーのみのリソースアクセス確認": [
                    "正常系_誰でもアクセスできるリソース",
                    "正常系_認証が必要なリソース",
                    "正常系_適切なユーザーのみが認証できる",
                    "異常系_不正なユーザーがアクセスしようとした場合のエラーレスポンス確認",
                ]
            },
        ],
    }
}

import pytest

from app.utils import logger


class TestAuth:
    logger.debug("### 認証と認可のテスト")
    logger.debug("### トークンベース認証の動作確認")

    @pytest.mark.django_db
    def test_正常系_トークンが発行される(self):
        pass

    @pytest.mark.django_db
    def test_正常系_トークンが正しい(self):
        pass

    @pytest.mark.django_db
    def test_異常系_トークンが発行されない(self):
        pass

    @pytest.mark.django_db
    def test_異常系_エラーレスポンスが返却される(self):
        pass

    logger.debug("### 適切なユーザーのみがリソースにアクセスできるかのテスト")

    @pytest.mark.django_db
    def test_正常系_誰でもアクセスできるリソース(self):
        pass

    @pytest.mark.django_db
    def test_正常系_認証が必要なリソース(self):
        pass

    @pytest.mark.django_db
    def test_正常系_適切なユーザーのみが認証できる(self):
        pass
