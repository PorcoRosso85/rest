from inline_snapshot import snapshot

session = {"user": {"id": 1, "name": "test", "email": "1@mail.com"}}


def test_ユーザー取得():
    assert session.get("user") == snapshot(
        {"id": 1, "name": "test", "email": "1@mail.com"}
    )
