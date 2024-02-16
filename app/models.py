from django.db import models
from django.utils import timezone


class Associate(models.Model):
    """Userの所属先であり 複数のSpaceを持つことができる"""

    PLAN_OPTIONS = [
        ("free", "Free"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="icon/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=100, choices=PLAN_OPTIONS, default="free")
    plan_created_at = models.DateTimeField(default=timezone.now)
    plan_updated_at = models.DateTimeField(default=timezone.now)


def get_default_associate() -> int:
    associate = Associate.objects.first()
    if associate:
        return associate.id
    new_associate = Associate.objects.create()
    return new_associate.id


class User(models.Model):
    """Userの情報を管理する"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associate = models.ManyToManyField(Associate, related_name="users")  # type: ignore


class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associate = models.ForeignKey(
        Associate,
        related_name="spaces",
        on_delete=models.CASCADE,
        default=get_default_associate,  # type: ignore
    )


def get_default_space() -> int:
    space = Space.objects.first()
    if space:
        return space.id
    new_space = Space.objects.create()
    return new_space.id


class ApiKeys(models.Model):
    """発行したAPIキーを管理する"""

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space = models.ForeignKey(
        Space,
        related_name="api_keys",
        on_delete=models.CASCADE,
        default=get_default_space,  # type: ignore
    )


def get_default_api_key() -> int:
    api_key = ApiKeys.objects.first()
    if api_key:
        return api_key.id
    new_api_key = ApiKeys.objects.create()
    return new_api_key.id


class Access(models.Model):
    """Associateの利用状況を管理する"""

    id = models.AutoField(primary_key=True)
    createad_at = models.DateTimeField(auto_now_add=True)
    api_key = models.ForeignKey(
        ApiKeys,
        related_name="access",
        on_delete=models.CASCADE,
        default=get_default_api_key,  # type: ignore
    )


class Structure(models.Model):
    """userが作成した構造(モデルと呼ばれる)を管理する"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    space = models.ForeignKey(
        Space,
        related_name="structures",
        on_delete=models.CASCADE,
        default=get_default_space,  # type: ignore
    )


def get_default_structure() -> int:
    structure = Structure.objects.first()
    if structure:
        return structure.id
    new_structure = Structure.objects.create()
    return new_structure.id


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    _title = models.CharField(max_length=100)
    _created_at = models.DateTimeField(auto_now_add=True)
    _updated_at = models.DateTimeField(auto_now=True)
    _published_at = models.DateTimeField(auto_now=True)
    structure = models.ForeignKey(
        Structure,
        related_name="data",
        on_delete=models.CASCADE,
        default=get_default_structure,  # type: ignore
    )
    value = models.JSONField(default=dict)  # type: ignore


def get_default_data() -> int:
    data = Data.objects.first()
    if data:
        return data.id
    new_data = Data.objects.create()
    return new_data.id


class PublishmentStatus(models.Model):
    STATUS_OPTIONS = [
        ("draft", "Draft"),
        ("review", "Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    status = models.CharField(max_length=100, choices=STATUS_OPTIONS, default="draft")
    data = models.ForeignKey(
        Data,
        related_name="status",
        on_delete=models.CASCADE,
        default=get_default_data,  # type: ignore
    )
    updated_at = models.DateTimeField(auto_now=True)
