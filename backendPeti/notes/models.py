from django.db import models
from userapp.models import User
from django import utils

class CutiHr(models.Model):
    sisa_cuti = models.CharField(max_length=24,  null=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)

    def __str__(self):
        return self.sisa_cuti

class NotesHrd(models.Model):
    employee_name = models.CharField(max_length=50, null=True)
    date_note = models.DateField(null=True, blank=True)
    notes = models.TextField(max_length=230, null=True)
    type_notes = models.CharField(max_length=120, null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=utils.timezone.now)
    updated_at = models.DateTimeField(auto_now= True)
    notes_optional = models.TextField(max_length=230, null=True, blank=True, default="optional")

    def save(self, *args, **kwargs):
            if(self.date_note != None ):
                self.day = self.date_note.day
                self.month = self.date_note.month
                self.year = self.date_note.year
                super(NotesHrd, self).save(*args, **kwargs)
            else:
                super(NotesHrd, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee_name

class EmployeeCuti(models.Model):
    employee_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    jatah_cuti = models.CharField(max_length=120, null=True)
    sisa_cuti = models.CharField(max_length=24,  null=True)
    tanggal_cuti = models.DateField(null=True, blank=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)
    catatan = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.sisa_cuti

