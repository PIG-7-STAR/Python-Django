import hashlib
from django.db import models
from django import utils
from userapp.models import User
import uuid

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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
    status_submission = models.BooleanField(null=True, blank=True, default=False)

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
        
        if(self.permission_pil != None):
            self.status_submission = True
        super(Submission, self).save(*args, **kwargs)

    def __str__(self):
        return self.permission_type
    
class CalendarCutiSubmission(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    permission_type = models.CharField(max_length=24,  null=True)
    reason = models.TextField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    color = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.title = self.employee.name
        hash_title = hashlib.md5(self.title.encode())
        hash_reason = hashlib.md5(self.reason.encode())
        hex_div = hash_reason.hexdigest()
        hash_hex = hash_title.hexdigest()
        dig2 = hash_hex[2:4]
        dig6 = hex_div[4:6]
        dig4 = hash_hex[5:7]
        self.color = '#'+dig2+dig4+dig6
        super(CalendarCutiSubmission, self).save(*args, **kwargs)

    def __str__(self):
        return self.permission_type