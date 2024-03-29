from django.contrib.auth.models import User, Group, AbstractUser, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

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

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's built-in `AbstractUser`.
    """
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

    USERNAME_FIELD = 'email'  # Default username field for authentication
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse('user-update', args=[str(self.pk)])


# class CustomGroup(Group):
#
#     def create_group(self, name, **extra_fields):
#         if not name:
#             raise ValueError("The given name must be set")
#         group = Group.objects.create(name=name, **extra_fields)
#         return group


class Equipment(models.Model):
    """
    Equipment model representing various types of equipment.
    """

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="equipments")
    is_available = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
