"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project import views
from project import helpers

urlpatterns = [
    path("admin/", admin.site.urls),
    path('add_user/', views.UserCreateView.as_view(), name="create-user"),
    path('add_group/', views.GroupCreateView.as_view()),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('main/', views.MainView.as_view(), name="main"),
    path('<int:pk>/update/', views.CustomUserUpdate.as_view(), name="user-update"),
    path('groups/', views.UserGroupsView.as_view(), name="user-groups"),
    path('group_details/', views.GroupDetailsView.as_view(), name="group-details"),
    path('<int:pk>/equipment_details/', views.EquipmentDetailView.as_view(), name="equipment-details"),
    path('users/', views.UsersView.as_view()),
    path('test/', helpers.TempUsersView.as_view()),
    # path('users-in-same-group/<int:group_id>/', views.UserInSameGroupListView.as_view(), name='users_in_same_group'),
    path('groups/<int:group_id>/users/', views.UsersInSameGroupView.as_view(), name='users_in_same_group'),
    path('create-equipment/', views.EquipmentCreate.as_view(), name='create-equipment'),
]
