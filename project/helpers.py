from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .models import CustomGroup, CustomUser
from project.forms import UserCreateForm, GroupCreateForm, LoginForm
from django.contrib.auth import authenticate, login, logout

#temporary view to testing groups in user
class TempUsersView(View):
    def get(self, request):
        user = CustomUser.objects.get(pk=5)
        groups = user.groups.all()
        return render(
            request,
            'testtemplate.html',
            context={
                'groups': groups
            }
        )