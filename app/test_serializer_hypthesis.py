import string

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase

from app.models import Content, Status
from app.serializer import SpaceSerializer


class TestSpaceSerializerHypothesis(HypothesisTestCase):
    def setup_method(self, method):
        self.status = Status.objects.create(status="draft")
        self.content = Content.objects.create(title="Test Content", status=self.status)

    def test_no_space(self):
        """
        Spaceオブジェクトが存在しない場合のテスト
        """
        serializer = SpaceSerializer(data={})
        assert not serializer.is_valid()

    # @given(
    #     from_model(
    #         Space,
    #         id=st.integers(min_value=1, max_value=100),
    #         content=st.lists(
    #             from_model(Content, id=st.integers(min_value=1, max_value=100))
    #         ),
    #     )
    # )
    # def test_space_no_content(self, space):
    #     """
    #     Spaceオブジェクトが存在するが、関連するContentオブジェクトが存在しない場合のテスト
    #     """
    #     space.content.set([self.content])
    #     space.save()
    #     serializer = SpaceSerializer(space)
    #     assert serializer.is_valid()
    #     assert serializer.errors == {"content": ["This field is required"]}

    #     # SpaceとContentの両方が存在するが、Contentが複数ある場合のテスト
    #     @given(
    #         from_model(Space),
    #         from_model(Content, space=from_model(Space)),
    #         from_model(Content, space=from_model(Space)),
    #     )
    #     def test_space_multiple_content(self, space, content1, content2):
    #         serializer = SpaceSerializer(
    #             data={"space": space.id, "content": [content1.id, content2.id]}
    #         )
    #         assert serializer.is_valid()

    #     # SpaceとContentの両方が存在し、Contentが異なるStatusを持つ場合のテスト
    #     @given(
    #         from_model(Space),
    #         from_model(Content, space=from_model(Space), status="draft"),
    #         from_model(Content, space=from_model(Space), status="published"),
    #     )
    #     def test_space_content_different_status(self, space, content1, content2):
    #         serializer = SpaceSerializer(
    #             data={"space": space.id, "content": [content1.id, content2.id]}
    #         )
    #         assert serializer.is_valid()

    # 異常な入力: Space オブジェクトの name フィールドに対して、空文字列や非常に長い文字列、特殊文字を含む文字列など、通常は想定されないような値を入力してみます。これにより、異常な入力に対するシステムのロバスト性を確認できます。
    @pytest.mark.django_db
    @given(st.text(min_size=95))
    def test_space_serializer_name(self, name):
        # logger.debug(f"name: {name}")
        serializer = SpaceSerializer(data={"name": name})
        assert not serializer.is_valid()

    # 境界値分析: Space オブジェクトの name フィールドに対して、最小長や最大長の文字列を入力してみます。これにより、境界値に対するシステムの挙動を確認できます。
    @pytest.mark.django_db
    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(blacklist_characters=string.digits),
        ),
    )
    def test_space_serializer_name_max(self, name):
        # logger.debug(f"name: {name}")
        serializer = SpaceSerializer(data={"name": name})
        assert not serializer.is_valid()

    # ランダムな入力: Space オブジェクトの name フィールドに対して、ランダムな文字列を入力してみます。これにより、予期せぬ入力に対するシステムの挙動を確認できます。

    # 依存関係のテスト: Space オブジェクトと Content オブジェクトの間の依存関係をテストします。例えば、Space オブジェクトに複数の Content オブジェクトを関連付けた場合や、Content オブジェクトを一つも関連付けなかった場合の挙動を確認します。

    # 逆方向の依存関係のテスト: Content オブジェクトから Space オブジェクトを参照する場合の挙動を確認します。例えば、Content オブジェクトが複数の Space オブジェクトに関連付けられている場合や、一つも関連付けられていない場合の挙動を確認します。
