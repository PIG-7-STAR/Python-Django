from django.db import models
from django import utils
from userapp.models import User
import hashlib

class Petitions(models.Model):
    employee_id = models.CharField(max_length=40, null=True)
    employee_name = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=120, null=True)
    permission_type = models.CharField(max_length=24,  null=True)
    reason = models.TextField(null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    jumlah_hari = models.IntegerField(null=True, blank=True)
    from_hour = models.IntegerField(null=True, blank=True)
    end_hour = models.IntegerField(null=True, blank=True)
    lembur_hour = models.IntegerField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    permission_pil = models.CharField( null=True, max_length=24, blank=True)
    reason_rejected = models.TextField( null=True, blank=True)
    conditional_reasons = models.TextField( null=True, blank=True)
    suspended_start = models.DateField( null=True, blank=True)
    suspended_end = models.DateField( null=True, blank=True)
    created_at = models.DateTimeField(default=utils.timezone.now)
    updated_at = models.DateTimeField(auto_now= True)

    def save(self, *args, **kwargs):
        if(self.end_hour != None and self.from_hour != None):
            calc = (int(self.end_hour) - int(self.from_hour))
            tle = len(str(calc))
            taw = tle-2
            slic = slice(taw,tle)
            dig = str(calc)
            finn = dig[slic]
            if(finn > '59'):
                ef = self.end_hour-100+60
                self.lembur_hour = (ef - self.from_hour)
                self.working_hour_detail = self.lembur_hour/100
            else:
                self.lembur_hour = calc
        super(Petitions, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_name
    
class PetitionsCalendar(models.Model):
    title = models.CharField(max_length=50, null=True)
    division = models.CharField(max_length=120, null=True)
    permission_type = models.CharField(max_length=24,  null=True)
    reason = models.TextField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    color = models.CharField(max_length=10, null=True, blank=True)
   
    def save(self, *args, **kwargs):
        hash_title = hashlib.md5(self.title.encode())
        hash_division = hashlib.md5(self.division.encode())
        hex_div = hash_division.hexdigest()
        hash_hex = hash_title.hexdigest()
        dig2 = hash_hex[2:4]
        dig6 = hex_div[4:6]
        dig4 = hash_hex[5:7]
        self.color = '#'+dig2+dig4+dig6
        super(PetitionsCalendar, self).save(*args, **kwargs)

    def __str__(self):
        return self.title