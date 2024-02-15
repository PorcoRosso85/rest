from django.db import models


class Structure(models.Model):
    """userが作成した構造(モデルと呼ばれる)を管理する"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""
draft, review, published, archived
StatusモデルのstatusフィールドはCharFieldで、choicesパラメータが設定されていますが、blank=Falseやnull=Falseといった制約が明示的に設定されていないため、空文字列("")を許容します。
DjangoのCharFieldはデフォルトでblank=False、null=Falseですが、これはデータベースレベルの制約であり、Pythonコードから直接モデルを操作する場合（例えばテストコードなど）は適用されません。Pythonコードから直接操作する場合、DjangoはCharFieldに対して空文字列を許容します。
statusフィールドに空文字列("")を許容しないようにするには、モデル定義でblank=Falseとnull=Falseを明示的に設定する必要があります。ただし、CharFieldに対してnull=Trueを設定することは推奨されません。空の値を表現するためには空文字列を使用するべきです。
また、choicesパラメータはフォームのバリデーション時にのみ適用され、モデルを直接操作する場合には適用されません。したがって、statusフィールドにchoicesで定義されていない値を設定することが可能です。
これらの制約を適用したい場合は、モデルのcleanメソッドをオーバーライドして、statusフィールドの値がSTATUS_OPTIONSに含まれるかどうかをチェックすることができます。
これは、DjangoのCharFieldがPythonレベルでは空文字列（""）を許容するためです。blank=Falseはフォームバリデーションに影響し、null=Falseはデータベースレベルの制約です。しかし、これらの制約はPythonコードから直接モデルを操作する場合には適用されません。
"""


class Status(models.Model):
    STATUS_OPTIONS = [
        ("draft", "Draft"),
        ("review", "Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    status = models.CharField(
        max_length=100, choices=STATUS_OPTIONS, blank=False, null=False
    )


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.ForeignKey(
        Structure, related_name="contents", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status, related_name="contents", on_delete=models.CASCADE, default=1
    )


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


class Associate(models.Model):
    """
    Userの所属先であり
    複数のSpaceを持つことができる
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="associates", on_delete=models.CASCADE)
    content = models.ForeignKey(
        Content, related_name="associates", on_delete=models.CASCADE
    )


class Space(models.Model):
    """
    どのAssosiatesがどのContentを持っているかを管理する
    AssosiatesとContentの中間テーブル
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associate = models.ManyToManyField(
        Associate, related_name="spaces", blank=True, null=True
    )
    content = models.ManyToManyField(
        Content, related_name="spaces", blank=True, null=True
    )
