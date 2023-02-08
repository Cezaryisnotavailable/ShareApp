from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import CustomGroup, CustomUser
from project.forms import UserCreateForm, GroupCreateForm, LoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# adding possibility to add group
class GroupCreateView(View):
    def get(self, request):
        form = GroupCreateForm()
        return render(request, "create_group.html", {"form": form})

    def post(self, request):
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Group.objects.create(name=data.get('name'))
        return HttpResponse("Group has been successfully registered")


# adding possibility to add user
class UserCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            group_name = data.get("group")
            group, created = Group.objects.get_or_create(name=group_name)
            # group = Group.objects.get(name=group_name)


            user = CustomUser.objects.create_user(
                username=data.get('login'),
                password=data.get('password'),
                email=data.get('email'),
            )
            user.groups.add(group.name)
        return HttpResponse("User has been successfully registered")


class MainView(View):
    def get(self, request):
        return render(request,'main.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(
            request,
            'login.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            # uwierzytelnienie
            user = authenticate(
                username=username,
                password=password
            )

            if user:
                # logowanie
                login(request, user)
                return HttpResponse(f"Zalogowano użytkownika {user}.")
            else:
                return HttpResponse(f"Błąd uwierzytelnienia. Podano nieprawidłowe poświadczenia.")


class LogoutView(View):
    def get(self, request):

        logout(request)
        return render(
            request,
            'logout.html'
        )