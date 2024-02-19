import pytest
from inline_snapshot import snapshot

from app.models import (
    Access,
    ApiKeys,
    Associate,
    Data,
    Space,
    Structure,
    User,
)


class TestApiKeysModel:
    @pytest.mark.django_db
    def test_正常系_Keyがユニークである(self):
        api_key1 = ApiKeys.objects.create()
        api_key2 = ApiKeys.objects.create()
        assert api_key1.api_key != api_key2.api_key

    @pytest.mark.django_db
    def test_正常系_Keyが自動生成される(self):
        api_key = ApiKeys.objects.create()
        assert api_key.api_key is not None

    @pytest.mark.django_db
    def test_正常系_関連するassociateのidを取得する(self):
        associate = Associate.objects.create()
        api_key = ApiKeys.objects.create(associate=associate)
        assert api_key.associate.id == associate.id

    @pytest.mark.django_db
    def test_異常系_関連するassociateが存在しない場合(self):
        associate = Associate.objects.create()
        api_key = ApiKeys.objects.create()
        assert api_key.associate.id != associate.id


class TestAccessModel:
    @pytest.mark.django_db
    def test_default_api_key(self):
        api_key = ApiKeys.objects.create()
        access = Access.objects.create()
        assert access.api_key.id == api_key.id

    @pytest.mark.django_db
    def test_generate_new_api_key(self):
        Access.objects.all().delete()
        ApiKeys.objects.all().delete()
        access = Access.objects.create()
        assert access.api_key is not None


class TestStructureModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        space = Space.objects.create()
        structure = Structure.objects.create(space=space)
        assert structure.space.id == space.id


class TestSpaceModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        space = Space.objects.create()
        assert space.id is not None

    @pytest.mark.django_db
    def test_正常系_Structureモデルを取得する場合(self):
        """Structureモデルを取得する場合"""
        space = Space.objects.create()
        structure = Structure.objects.create(space=space)
        assert space.structures.first().id == structure.id

    # structureが関連するspaceのためのstructure.idを返せているかを確認する
    @pytest.fixture
    def fixture_space(self):
        # 複数のspaceを作成する
        return [Space.objects.create() for _ in range(3)]

    @pytest.fixture
    def fixture_structure(self, fixture_space):
        # spaceに関連するstructureを作成する
        related_structure = [
            Structure.objects.create(space=space) for space in fixture_space
        ]
        # 各spaceとは関連しないstructureを作成する
        unrelated_structure = [Structure.objects.create() for _ in range(3)]

        return related_structure, unrelated_structure

    @pytest.mark.django_db
    def test_正常系_関連するstructureを取得する場合(
        self, fixture_space, fixture_structure
    ):
        """関連するstructureを取得する場合"""
        related_structure, unrelated_structure = fixture_structure
        for i, space in enumerate(fixture_space):
            # logger.debug(f"### space: {space}")
            # logger.debug(f"### related_structure[i]: {related_structure[i]}")
            assert list(space.structures.all()) == [related_structure[i]]

        for i, space in enumerate(fixture_space):
            # logger.debug(f"### space: {space}")
            # logger.debug(f"### unrelated_structure[i]: {unrelated_structure[i]}")
            assert list(space.structures.all()) != [unrelated_structure[i]]

    # 関連するstructureが複数ある場合に正しく取得できるかを確認する
    @pytest.fixture
    def fixture_related_structure(self, fixture_space: list[Space]) -> list[Structure]:
        # spaceに関連するstructureを作成する
        return [Structure.objects.create(space=space) for space in fixture_space]

    @pytest.fixture
    def fixture_related_structures(
        self, fixture_space: list[Space]
    ) -> list[list[Structure]]:
        # 各spaceに関連する複数のstructureを作成する
        structures = []
        for space in fixture_space:
            structures_for_space = [
                Structure.objects.create(space=space) for _ in range(2)
            ]  # 各Spaceに2つのStructureを関連付ける
            structures.append(structures_for_space)
        return structures

    @pytest.mark.django_db
    def test_正常系_関連するstructureが複数ある場合に正しく取得できるかを確認する(
        self, fixture_space, fixture_related_structures
    ):
        """関連するstructureが複数ある場合に正しく取得できるかを確認する"""
        for i, space in enumerate(fixture_space):
            expected_structures = fixture_related_structures[i]
            actual_structures = list(space.structures.all())
            assert sorted(actual_structures, key=lambda s: s.id) == sorted(
                expected_structures, key=lambda s: s.id
            )

    @pytest.fixture
    def fixture_space_one(self) -> Space:
        return Space.objects.create(id=9)

    @pytest.fixture
    def fixture_structures_for_space_one(
        self, fixture_space_one: Space
    ) -> list[Structure]:
        structure_ids = [9, 8, 7]
        return [
            Structure.objects.create(id=id, space=fixture_space_one)
            for id in structure_ids
        ]

    @pytest.mark.django_db
    def test_正常系_関連するstructureが複数ある場合に正しく取得できるかを確認する_for_space_one(
        self, fixture_space_one, fixture_structures_for_space_one
    ):
        """関連するstructureが複数ある場合に正しく取得できるかを確認する"""
        expected_structure_ids = [9, 8, 7]
        actual_structure_ids = [
            structure.id for structure in fixture_space_one.structures.all()
        ]
        assert sorted(actual_structure_ids) == sorted(expected_structure_ids)


class TestAssociateModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        associate = Associate.objects.create()
        assert associate.id is not None

    @pytest.mark.django_db
    def test_正常系_関連するspaceとapi_keyを取得する場合(self):
        """関連するspaceとapi_keyを取得する場合"""
        associate = Associate.objects.create()
        api_key = ApiKeys.objects.create(associate=associate)
        assert associate.api_keys.first().id == api_key.id

    @pytest.mark.django_db
    def test_正常系_関連するspaceとapi_keyとaccessを取得する場合(self):
        """関連するspaceとapi_keyとaccessを取得する場合
        Associate
           |
           ApiKeys
              |
             Access
                |
              (access)
        """
        associate = Associate.objects.create()
        api_key = ApiKeys.objects.create(associate=associate)
        access = Access.objects.create(api_key=api_key)
        assert associate.api_keys.first().access.first().id == access.id
        assert associate.api_keys.first().access.first().api_key.id == api_key.id


class TestUserModel:
    @pytest.mark.django_db
    def test_正常系_クエリが成功する場合(self):
        """クエリが成功する場合"""
        user = User.objects.create()
        assert user.id is not None

    @pytest.mark.django_db
    def test_正常系_関連するassociateを取得する場合(self):
        """関連するassociateを取得する場合"""
        user = User.objects.create()
        associate = Associate.objects.create()
        user.associates.add(associate)
        assert user.associates.first().id == associate.id

    @pytest.mark.django_db
    def test_正常系_関連するassociateとspaceとapi_keyを取得する場合(self):
        """関連するassociateとspaceとapi_keyを取得する場合
        user[1, 2]が同じassociate[1]に所属している
        """
        user1 = User.objects.create()
        user2 = User.objects.create()
        associate = Associate.objects.create()
        api_key = ApiKeys.objects.create(associate=associate)
        user1.associates.add(associate)
        user2.associates.add(associate)
        # assert (
        #     user1.associates.first().spaces.first().api_keys.first().id
        #     == user2.associates.first().spaces.first().api_keys.first().id
        # )
        assert (
            user1.associates.first().api_keys.first().id
            == user2.associates.first().api_keys.first().id
        )

    @pytest.mark.django_db
    def test_正常系_関連するassociateとspaceとapi_keyを取得する場合(self):
        """関連するassociateとspaceとapi_keyを取得する場合
        user[1, 2]が同じassociate[1]に所属している
        user[3]は異なるassociate[2]に所属している
        """
        user1 = User.objects.create()
        user2 = User.objects.create()
        user3 = User.objects.create()
        associate1 = Associate.objects.create()
        associate2 = Associate.objects.create()
        api_key1 = ApiKeys.objects.create(associate=associate1)
        api_key2 = ApiKeys.objects.create(associate=associate2)
        user1.associates.add(associate1)
        user2.associates.add(associate1)
        user3.associates.add(associate2)

        # user1とuser2が同じassociate1に所属していることを検証
        assert user1.associates.first().api_keys.first().id == api_key1.id
        assert user2.associates.first().api_keys.first().id == api_key1.id

        # user3が異なるassociate2に所属していることを検証
        assert user3.associates.first().id == associate2.id
        assert not user3.associates.first().api_keys.first().id == api_key1.id
        assert user3.associates.first().api_keys.first().id == api_key2.id


class TestDataModel:
    @pytest.mark.django_db
    def test_modelフィールドにはJson形式のデータを保存できる(self):
        data = Data.objects.create(_model={"1": {"2": {"3": [1, 2, 3]}}})
        assert data._model == snapshot({"1": {"2": {"3": [1, 2, 3]}}})
