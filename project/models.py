
from django.contrib.auth.models import User, Group, AbstractUser
from django.db import models


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


    USERNAME_FIELD = 'email' #zakladnie kont przez email dla weryfikacji
    REQUIRED_FIELDS = ['groups']



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
