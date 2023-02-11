
from django.contrib.auth.models import User, Group, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


CATEGORIES = (
    (1, "Cars"),
    (2, "Tools"),
    (3, "RTV"),
    (4, "AGD"),
    (5, "Coworking office")
)
#
# class AddGroupInfo(models.Model):
#     group = models.OneToOneField("Group")

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = 'email' #zakladnie kont przez email dla weryfikacji
    REQUIRED_FIELDS = ['username']



class CustomGroup(Group):

    def create_group(self, name, **extra_fields):
        if not name:
            raise ValueError("The given name must be set")
        group = Group.objects.create(name=name, **extra_fields)
        return group


class Equipment(models.Model):
    name = models.CharField(max_length=150)
    category = models.IntegerField(choices=CATEGORIES)
    is_available = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
