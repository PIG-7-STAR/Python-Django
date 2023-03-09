from django.db import models
from userapp.models import User
from django import utils
from datetime import datetime

class NotesApp(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_note = models.DateField(null=False, blank=False)
    notes = models.TextField(max_length=230, null=False, blank=False)
    type_notes = models.CharField(max_length=120, null=False, blank=False)
    hari = models.IntegerField(null=True, blank=True)
    bulan = models.IntegerField(null=True, blank=True)
    tahun = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=utils.timezone.now)
    updated_at = models.DateTimeField(auto_now= True)
    name_day = models.CharField(max_length=120, null=True, blank=True)

    # notes_optional = models.TextField(max_length=230, null=True, blank=True, default="optional")

    def save(self, *args, **kwargs):
            if(self.date_note != None ):
                if(self.name_day != '' and self.bulan != ''):
                    cr_date = datetime.strptime(self.date_note, '%Y-%m-%d')
                    self.hari = cr_date.day
                    self.bulan = cr_date.month
                    self.tahun = cr_date.year
                    self.name_day = cr_date.strftime('%A')

                    # self.hari = self.date_note.day
                    # self.bulan = self.date_note.month
                    # self.tahun = self.date_note.year
                    # self.name_day = self.date_note.strftime('%A')
                    super(NotesApp, self).save(*args, **kwargs)
                else:
                    # cr_date = datetime.strptime(self.date_note, '%Y-%m-%d')
                    # self.hari = cr_date.day
                    # self.bulan = cr_date.month
                    # self.tahun = cr_date.year
                    # self.name_day = cr_date.strftime('%A')

                    self.hari = self.date_note.day
                    self.bulan = self.date_note.month
                    self.tahun = self.date_note.year
                    self.name_day = self.date_note.strftime('%A')

                    super(NotesApp, self).save(*args, **kwargs)
            # else:
                # super(NotesApp, self).save(*args, **kwargs)

    def __str__(self):
        return self.employee.name