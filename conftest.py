import pytest

from project.models import CustomUser, Equipment
from django.test import Client


@pytest.fixture()
def user_1(db):
    user = CustomUser.objects.create_user("test-user")
    return user

@pytest.fixture()
def new_user_factory():
    def create_app_user(
            username: str,
            password: str = None,
            first_name: str = "firstname",
            last_name: str = "lastname",
            email: str = "test@test.com.pl",
            is_staff: str = False,
            is_superuser: str = False,
            is_active: str = True,
    ):
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active
        )
        return user
    return create_app_user

@pytest.fixture
def new_user(db, new_user_factory):
    return new_user_factory("Test_user", "password", "MyName", email="test@test.com.pl")

@pytest.fixture
def client(db):
    client = Client()
    return client


@pytest.fixture
def equipment():
    return Equipment.objects.create(
        name="Hammer",
        category="Tools",
        is_available=True,
        user=new_user
    )
