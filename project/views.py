from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from .models import CustomUser, Equipment
from project.forms import UserCreateForm, GroupCreateForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

# adding possibility to add group
class GroupCreateView(View):
    """
     A view that handles creating a new group. (Group can be created only by admin - to be implemented)
    """
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
    """
    A view that handles requests to display and process a form for creating a new user with the option to assign them to
     a pre-existing group.
    """
    def get(self, request):
        form = UserCreateForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        print("*" * 20)
        print(form.errors) # bledy walidacji z formularza
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
    """
     A simple view that displays the main page of the website.
    """
    def get(self, request):
        return render(request,'main.html')


# Opening session
class LoginView(View):
    """
    A view that displays a login form and handles user authentication.
    """
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
    """
    A view that logs out the current user.
    """
    def get(self, request):

        logout(request)
        return redirect("/main/")

#Adding a list of groups to which the CustomUser is assigned
class UserGroupsView(ListView):
    """
    A view that displays a list of groups to which the logged-in user is assigned
    """
    model = CustomUser
    template_name = "groups_list.html"
    context_object_name = "users"
    def get_queryset(self):
        user_groups = CustomUser.objects.filter(username=self.request.user.username) #filter by logged in user
        # print(user_groups[0].groups.all())
        return user_groups

#list of users - to be modified to be avaiable only for Admin
class UsersView(ListView):
    """
    A view that displays a list of all users (should be restricted to admin users only - to be implemented).
    """
    model = CustomUser
    template_name = "users_view.html"
    context_object_name = "users"


# allows to change username and dynamically reverses (reverse_lazy) to the main site
class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username"]
    template_name = "customuser_update_form.html"
    success_url = reverse_lazy("main")


class EquipmentCreate(LoginRequiredMixin, CreateView):
    """
    A view that handles creating new equipment objects.
    """
    model = Equipment
    fields = ['name', 'category', 'is_available']
    template_name = "equipment_form.html"
    success_url = reverse_lazy("user-groups")

    def form_valid(self, form):
        """
        the user field of the new Equipment instance will be set to the currently logged-in user
        :param form:
        :return:
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    """
    A view that displays the details of a specific equipment object
    """
    model = Equipment
    template_name = 'equipment_detail.html'
    context_object_name = 'equipment'


class GroupDetailsView(LoginRequiredMixin, DetailView):
    """
    A view that displays the details of a specific group.
    """
    pass


# class UserInSameGroupListView(LoginRequiredMixin, ListView):
#     model = CustomUser
#     template_name = 'users_in_same_group.html'
#     context_object_name = 'users'
#
#     def get_queryset(self):
#         user = self.request.user
#         group_ids = user.groups.values_list("id", flat=True)
#         return CustomUser.objects.filter(groups__id__in=group_ids).exclude(id=user.id)


# Showing users in the same group regardless of other groups to which the given user may be assigned
class UsersInSameGroupView(TemplateView):
    """
     A view that displays a list of users who belong to the same group as the specified group ID.
    """
    template_name = 'users_in_same_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get('group_id')
        group = Group.objects.get(pk=group_id)
        context['group_name'] = group.name
        context['users'] = group.user_set.all()
        return context