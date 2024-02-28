import json
import logging
import subprocess

import pytest
from inline_snapshot import snapshot

logger = logging.getLogger(__name__)

PROJECT_NAME = "init240225"
PROJECT_NUMBER = "917702307080"
PROJECT_ID = "init240225"
BILLING_ACCOUNT = "019653-71A4BD-7ED1A6"


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output


def test_run_command():
    output = run_command("gcloud config list")
    logger.info(f"### output: {output}")
    assert b"1.is.universe@gmail.com" in output

    # output = run_command("docker build .")
    # assert b"Sending build context to Docker daemon" in output


class Testアプリ:
    @pytest.mark.skip
    def test200_cloudsqlの接続情報が暗号化できている(self):
        # gcloud CLIを使用してCloud SQLの接続情報を取得
        command = "gcloud sql instances describe [INSTANCE_ID]"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        # 出力をJSONとして解析
        instance_info = json.loads(output)

        # 接続名が暗号化されていることを確認
        assert instance_info["connectionName"].startswith("encrypted:")

        # ユーザー名とパスワードが暗号化されていることを確認
        assert instance_info["settings"]["userLabels"]["username"].startswith(
            "encrypted:"
        )
        assert instance_info["settings"]["userLabels"]["password"].startswith(
            "encrypted:"
        )

    def test200_DjangoでGoogleCloudPythonConnectorを設定できている(self):
        # settings.pyにGoogleCloudPythonConnectorの設定を追加
        settings = "settings.py"
        with open(settings, "a") as f:
            f.write(
                """
                DATABASES = {
                    'default': {
                        'ENGINE': 'google.cloud.sql.connector.django',
                        'INSTANCE': 'project:region:instance',
                        'NAME': 'database_name',
                        'USER': 'username',
                        'PASSWORD': 'password',
                        
                    }}
                """
            )

    @pytest.mark.skip
    def test200_DjangoでCloudSQLに接続できている(self):
        # Djangoアプリケーションを起動
        output = run_command("python manage.py runserver")
        assert b"Starting development server at http://localhost:8000/" in output

        # ブラウザでアプリケーションにアクセス
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        assert b"Connected to database" in output
        # データベースに接続できていることを確認
        output = run_command(
            "curl http://localhost:8000/ | grep 'Connected to database'"
        )
        # アプリケーションが正常に動作していることを確認
        # ブラウザでアプリケーションにアクセスし、Cloud SQLに接続できていることを確認
        # ブラウザでアプリケーションにアクセスし、データベースのデータを取得できることを確認


class Testビルド:
    def test200_Dockerfileを作成する(self):
        # ベースイメージを選択する
        # 必要なライブラリをインストールする
        # アプリケーションコードをコピーする
        # コマンドを実行する
        pass

    def tsst200_GoogleCloudBuildでビルドする(self):
        # ビルド構成ファイルをローカルで作成する
        # ビルドを実行する
        # ビルド結果を確認する
        pass


class Testデプロイ:
    class Test200_VPCを設定する:
        @pytest.mark.skip
        def test200_VPCの作成(self):
            run_command(
                "gcloud compute networks create vpcinit240227 --subnet-mode=auto"
            )
            pass

        def test200_サブネットの作成(self):
            # サブネットの作成
            pass

        def test200_ファイアウォールの設定(self):
            # ファイアウォールの設定
            pass

    class Test200_ネットワーク設定をする:
        def test200_サービスの公開範囲(self):
            # サービスの公開範囲
            pass

        def test200_IPアドレスの許可範囲(self):
            # IPアドレスの許可範囲
            pass

        def test200_ロードバランサーの設定(self):
            # ロードバランサーの設定
            pass

    class Test200_認証と認可をする:
        # IAMの設定
        def test200_IAMの設定(self):
            # エンティティの作成
            # ロールの割り当て
            # ポリシー・権限範囲の決定
            # サービスアカウントのキー付与
            pass

        # APIキーの設定
        def test200_APIキーの設定(self):
            # APIキーの作成
            # APIキーの使用
            pass

        # OAuth2.0の設定: 安全にサービスアカウントキーを認証するプロトコルを使用するかのオプション

        # RBACの設定: Cloud RunにCloud SQLへのアクセス権を付与する
        def test200_RBACの設定(self):
            # ロールの作成
            # ロールの割り当て
            # ポリシーの作成
            pass


class Testメンテナンス:
    class Test200_リソースを監視する:
        def test200_コストを監視する(self):
            # コストを監視する
            assert run_command(
                f"gcloud billing projects list --billing-account={BILLING_ACCOUNT}"
            ) == snapshot(b"")
            assert run_command(
                f"gcloud billing projects describe {PROJECT_ID} --format=json"
            ) == snapshot(
                b'{\n  "billingAccountName": "",\n  "billingEnabled": false,\n  "name": "projects/init240225/billingInfo",\n  "projectId": "init240225"\n}\n'
            )
