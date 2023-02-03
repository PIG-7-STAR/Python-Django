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
        name = models.CharField(max_length=255, blank=True, null=True)
        division = models.CharField(max_length=255, blank=True, null=True)
        is_active = models.BooleanField(default=True) #karyawan aktif
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        employee_joined = models.DateField(null=True, blank=True)
        date_joined = models.DateTimeField(default=timezone.now) #karyawan mulai bekerja
        receive_newsletter = models.BooleanField(default=False)
        sisa_cuti = models.CharField(max_length=20, blank=True, null=True)
        birth_date = models.DateField(blank=True, null=True)
        address = models.CharField(max_length=300, blank=True, null=True)
        roles = models.CharField(max_length=30, blank=True, null=True)
        gender = models.CharField(max_length=30, blank=True, null=True)
        religion = models.CharField(max_length=30, blank=True, null=True)
        employee_code = models.CharField(max_length=250, blank=True, null=True, default="EmpId")
 
        objects = UserManager()

        def save(self, *args, **kwargs):
            if(self.first_name != None and self.last_name != None):
                self.name = (self.first_name + ' ' + self.last_name)
                super(User, self).save(*args, **kwargs)
            else:
                super(User, self).save(*args, **kwargs)
            

        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS =  [ 'email', ]

class UserRoles(models.Model):
    roles = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.roles

class UserDivision(models.Model):
    division = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.division