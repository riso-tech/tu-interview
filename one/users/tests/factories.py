from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from one.users.models import Company, Department, Position


class CompanyFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = Company


class DepartmentFactory(DjangoModelFactory):
    name = Faker("name")
    company = SubFactory(CompanyFactory)

    class Meta:
        model = Department


class PositionFactory(DjangoModelFactory):
    name = Faker("name")
    department = SubFactory(DepartmentFactory)

    class Meta:
        model = Position


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    first_name = Faker("name")
    company = SubFactory(CompanyFactory)
    department = SubFactory(DepartmentFactory)
    position = SubFactory(PositionFactory)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
