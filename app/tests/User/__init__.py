"""
認証と認可のテスト
トークンベース認証の動作確認
適切なユーザーのみがリソースにアクセスできるかのテスト

アカウント情報の取得
ログインユーザーのアカウント情報が正しく取得できること
存在しないユーザーのアカウント情報を取得しようとした場合は、エラーレスポンスが返却されること

アカウント情報の更新
アカウント情報を更新できること
更新内容が正しく反映されること
不正な値を更新しようとした場合は、エラーレスポンスが返却されること

パスワード変更
ログインユーザーのパスワードを変更できること
パスワードが正しく変更されること
不正なパスワードを入力した場合は、エラーレスポンスが返却されること

2要素認証の設定
2要素認証アプリを登録できること
2要素認証が有効になること
2要素認証アプリの登録に失敗した場合は、エラーレスポンスが返却されること

アカウント削除
アカウントを削除できること
アカウント情報が正しく削除されること
アカウント削除に失敗した場合は、エラーレスポンスが返却されること

APIエンドポイントのテスト
GETリクエストで正しいJSONレスポンスが返るか
POSTリクエストによるデータの作成と適切なレスポンスコードの確認
PUT/PATCHリクエストによるデータ更新のテスト
DELETEリクエストでデータが削除されるか

シリアライザのテスト
リクエストデータのシリアライズの正確性
レスポンスデータのデシリアライズの正確性

エラーハンドリングのテスト
不正なリクエストに対するエラーレスポンスの検証
予期せぬエラーが発生した場合の処理

パフォーマンスのテスト
大量のリクエストを処理できるか
応答時間の計測"""

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


class TestGetAccountInfo:
    logger.debug("### ログインユーザーのアカウント情報が正しく取得できること")

    # ユーザーがデータベースに存在することを確認
    @pytest.mark.django_db
    def test_正常系_ユーザーが存在する(self):
        pass

    # 認証情報をリクエストヘッダに付与
    @pytest.mark.django_db
    def test_正常系_認証情報をリクエストヘッダに付与されている(self):
        pass

    # ログインリクエストを送信
    # レスポンスのステータスコードを確認
    @pytest.mark.django_db
    def test_正常系_ログインリクエストを送信(self):
        pass

    @pytest.mark.django_db
    def test_正常系_アカウント情報が取得できる(self):
        pass

    @pytest.mark.django_db
    def test_正常系_アカウント情報が正しい(self):
        pass

    logger.debug(
        "### 存在しないユーザーのアカウント情報を取得しようとした場合は、エラーレスポンスが返却されること"
    )

    @pytest.mark.django_db
    def test_異常系_ユーザーが存在しない(self):
        pass

    @pytest.mark.django_db
    def test_異常系_エラーレスポンスが返却される(self):
        pass

    logger.debug("### アカウント情報の更新")
