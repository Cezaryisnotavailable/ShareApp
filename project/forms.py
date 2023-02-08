from django import forms
from django.contrib.auth.models import User, Group

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from project.models import CustomUser


# creating user with assignment to a pre-created group
class UserCreateForm(forms.Form):
    CHOICES = (
        (group.id, f"{group}") for group in Group.objects.all()
    )
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    # group = forms.ChoiceField(choices=CHOICES)
    group = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasła nie są identyczne")

    def clean_login(self):
        user_name = self.cleaned_data.get('login')
        user = CustomUser.objects.filter(username=user_name)
        if user:
            raise ValidationError("Podana nazwa użytkownika jest już zarezerwowana")

        return user_name


# to bedzie raczej
class GroupCreateForm(forms.Form):
    name = forms.CharField()


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)






