import pytest
from django.urls import reverse

# from project.forms import UserCreateForm
from project.models import CustomUser


@pytest.mark.django_db
def test_set_check_password(user_1):
    user_1.set_password("new-password")
    assert user_1.check_password("new-password") is True

@pytest.mark.django_db
def test_new_user(new_user):
    print(new_user.first_name)
    assert new_user.first_name == "MyName"


@pytest.mark.django_db
def test_user_create_view(client):
    response = client.get(reverse("create-user"))
    assert response.status_code == 200
    print(f"test pierwszy")

    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'password2': 'testpassword',
        'email': 'testuser@example.com',
        'group': 2,
    }
    # form = UserCreateForm(data=data)
    # assert form.is_valid()

    response = client.post(reverse("create-user"), data=data)
    assert response.status_code == 302
    print(f"test drugi")

    user = CustomUser.objects.get(email='testuser@example.com')
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    # assert user.groups.filter(name='Grupa1').exists()

def test_main_view(client):
    url = reverse("main")
    response = client.get(url)
    assert response.status_code == 200
    assert 'App to share your eq' in response.content.decode('utf-8')


def test_login_view(client, new_user):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'E-mail': new_user.email,
        'Password': "password",
    }
    print(data.get('E-mail'))
    print(data.get('Password'))

    response = client.post(url, data)

    assert response.status_code == 302  # redirect to /main/ on successful login
    assert response.url == '/main/'

    # # create a user with wrong credentials
    # CustomUser.objects.create_user(username='testuser2', password='testpassword2')
    #
    # data = {
    #     'username': 'testuser2',
    #     'password': 'wrongpassword',
    # }
    #
    # response = client.post(url, data)
    #
    # assert response.status_code == 200  # failed login should return 200
    # assert f'Błąd uwierzytelnienia' in response.content

@pytest.mark.django_db
def test_equipment_detail_view(client, equipment):
    client.force_login(email="admin@admin.com")
    response = client.get("2/equipment_details/")
    assert response.status_code == 200
    assert response.context.get('name') == "Hammer"


