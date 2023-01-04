from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_active, is_staff, is_superuser, **extrafields):
        now = timezone.now()
        if not username:
            raise ValueError("the given username is not valid")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_active=is_active, 
                            is_staff=is_staff, is_superuser=is_superuser, date_joined=now, **extrafields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password, **extrafields):
        return self._create_user(username, email, password, is_active=True, is_staff=False, is_superuser=False, **extrafields)

    def create_superuser(self, username, email, password, **extrafields):
        user = self._create_user(username, email, password, is_active=True, is_staff=True, 
                                is_superuser=True, **extrafields)
        user.save(using=self._db)

        return user    

class User(AbstractBaseUser, PermissionsMixin):
        username= models.CharField(max_length=120, unique=True)
        email = models.EmailField(max_length=250, unique=True)
        first_name = models.CharField(max_length=30, blank=True, null=True)
        last_name = models.CharField(max_length=30, blank=True, null=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        date_joined = models.DateTimeField(default=timezone.now)
        receive_newsletter = models.BooleanField(default=False)
        sisa_cuti = models.CharField(max_length=20, blank=True, null=True)
        birth_date = models.DateTimeField(blank=True, null=True)
        address = models.CharField(max_length=300, blank=True, null=True)
        roles = models.CharField(max_length=30, blank=True, null=True)
        city = models.CharField(max_length=30, blank=True, null=True)

        objects = UserManager()

        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS =  [ 'email', ]