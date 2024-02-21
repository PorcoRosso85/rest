import os

env = {
    "SECRET_KEY": os.environ.get("SECRET_KEY"),
    # "BASE_DIR": os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "DJANGO_SETTINGS_MODULE": os.environ.get("DJANGO_SETTINGS_MODULE"),
}


class TestConfig:
    def test_正常系_環境変数が取得できる場合(self):
        """環境変数が取得できる場合"""
        # assert (
        #     env["SECRET_KEY"]
        #     == "django-insecure-+_u=p74&cce8w2_ot15o3ua&zn65e@!m#)&1oiclcep8*%^wfy"
        # )

        assert env["DJANGO_SETTINGS_MODULE"] == "core.settings"
