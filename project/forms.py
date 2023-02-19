from django import forms
from django.contrib.auth.models import User, Group

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from project.models import CustomUser


# creating user with assignment to a pre-created group
class UserCreateForm(forms.Form):
    """
    A form used for creating a user with assignment to a pre-created group by admin.
    """
    CHOICES = (
        (group.id, f"{group}") for group in Group.objects.all() # w widoku sprawdzic
    )
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    # group = forms.ChoiceField(choices=CHOICES)
    group = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def clean(self):
        """
        Validates the password fields to ensure they match.
        :return:
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        print("*" * 20) # w finalnym kodzie usunac
        print(password)
        password2 = cleaned_data.get('password2')
        print("*" * 20)
        print(password2)
        if password != password2:
            raise ValidationError("Podane hasła nie są identyczne")

    def clean_login(self):
        """
        Validates that the entered username is not already taken.
        :return:
        """
        user_name = self.cleaned_data.get('username')
        user = CustomUser.objects.filter(username=user_name)
        if user:
            raise ValidationError("Podana nazwa użytkownika jest już zarezerwowana")

        return user_name



class GroupCreateForm(forms.Form):
    """
    A form used for creating a new group.
    """
    name = forms.CharField()


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    """
    A form used for logging in a user.
    """
    username = forms.CharField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput)






