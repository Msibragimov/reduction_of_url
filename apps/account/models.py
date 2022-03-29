from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models

from apps.account.manager import UserManager
from apps.account.model_fields import LowercaseEmailField


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=15)
    email = LowercaseEmailField(unique=True)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    bio = models.CharField(max_length=800)
    profile_photo = models.ImageField(upload_to='media/images/', null=True, default='photo.jpg')
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_perms(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class UserConfirmCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.PositiveIntegerField()
    sended = models.DateTimeField(default=timezone.now)