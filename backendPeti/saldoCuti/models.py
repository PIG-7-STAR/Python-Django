from django.db import models
from userapp.models import User

class SaldoCuti(models.Model):
    saldo_cuti = models.CharField(max_length=24,  null=True)
    sisa_cuti = models.CharField( max_length=24, null=True, blank=True)
    userprofiles = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.saldo_cuti