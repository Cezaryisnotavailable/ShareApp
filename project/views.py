from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from .models import CustomGroup, CustomUser, Equipment
from project.forms import UserCreateForm, GroupCreateForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
                username=data.get('username'),
                password=data.get('password'),
                email=data.get('email'),
            )
            user.groups.add(group.name)
        return HttpResponse("User has been successfully registered")


class MainView(View):
    def get(self, request):
        return render(request,'main.html')


# Opening session
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
            print("*"*20)
            print(username, password)
            # uwierzytelnienie
            user = authenticate(
                username=username,
                password=password
            )
            print(user)
            if user:
                # logowanie
                login(request, user)
                return redirect("/main/")
            else:
                return HttpResponse(f"Błąd uwierzytelnienia. Podano nieprawidłowe poświadczenia.")


# Closing session
class LogoutView(View):
    def get(self, request):

        logout(request)
        return redirect("/main/")

#Adding a list of groups to which the CustomUser is assigned
class UserGroupsView(ListView):
    model = CustomUser
    template_name = "groups_list.html"
    context_object_name = "users"
    def get_queryset(self):
        user_groups = CustomUser.objects.filter(username=self.request.user.username) #filter by logged in user
        # print(user_groups[0].groups.all())
        return user_groups

#list of users - to be modified to be avaiable only for Admin
class UsersView(ListView):
    model = CustomUser
    template_name = "users_view.html"
    context_object_name = "users"


# allows to change username and dynamically reverses (reverse_lazy) to the main site
class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username"]
    template_name = "customuser_update_form.html"
    success_url = reverse_lazy("main")


class EquipmentCreate(CreateView):
    model = Equipment
    fields = ['__all__']
    success_url = reverse_lazy("main")


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment_detail.html'
    context_object_name = 'equipment'


class GroupDetailsView(LoginRequiredMixin, DetailView):
    pass