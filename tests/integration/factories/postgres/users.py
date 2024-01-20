import uuid

import factory  # type: ignore
from factory import Sequence
from faker import Faker

from src.core.auth import Roles
from src.modules.users.models import Users
from tests.integration.factories.postgres.base import BaseFactory

fake = Faker("ru_RU")


class UsersFactory(BaseFactory):
    class Meta:
        model = Users

    id = factory.LazyFunction(uuid.uuid4)
    username = factory.LazyFunction(fake.user_name)
    hashed_password = factory.LazyFunction(fake.password)
    email = factory.LazyFunction(fake.email)
    phone = Sequence(lambda n: fake.numerify("7##########"))
    role = Roles.USER
    is_deleted = factory.LazyAttribute(
        lambda obj: fake.boolean(chance_of_getting_true=10)
    )
    created_at = factory.LazyFunction(fake.date_time)
    updated_at = factory.LazyFunction(fake.date_time)
