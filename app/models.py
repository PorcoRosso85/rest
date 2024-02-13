from django.db import models


class Structure(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


import pytest


@pytest.fixture
def structure():
    return Structure.objects.create(
        name="Test Structure",
        description="Test Description",
    )


@pytest.mark.django_db
def test_structure(structure):
    assert structure.name == "Test Structure"
    assert structure.description == "Test Description"
    assert structure.created_at
    assert structure.updated_at
