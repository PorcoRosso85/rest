from django.db import models


class Space(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_default_space() -> int:
    space = Space.objects.first()
    if space:
        return space.id
    new_space = Space.objects.create()
    return new_space.id


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


class Plan(models.Model):
    """
    Userのプランを管理する
    'free', 'standard', 'premium'
    """

    PLAN_OPTIONS = [
        ("free", "Free"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    name = models.CharField(max_length=100, choices=PLAN_OPTIONS)


class User(models.Model):
    """
    Userの情報を管理する
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, related_name="users", on_delete=models.CASCADE)


class Usage(models.Model):
    """Associateの利用状況を管理する"""

    data_transported = models.IntegerField()
    api_requested = models.IntegerField()
    createad_at = models.DateTimeField(auto_now_add=True)


class Associate(models.Model):
    """
    Userの所属先であり
    複数のSpaceを持つことができる
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="icon/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(
        User, related_name="associates", on_delete=models.CASCADE
    )
    space = models.ForeignKey(
        Space, related_name="associates", on_delete=models.CASCADE, null=True
    )
    usage = models.ForeignKey(
        Usage, related_name="associates", on_delete=models.CASCADE, null=True
    )
