from django.db import models

class NotesHrd(models.Model):
    employee_name = models.CharField(max_length=50, null=True)
    jatah_cuti = models.CharField(max_length=120, null=True)
    sisa_cuti = models.CharField(max_length=24,  null=True)
    tanggal_cuti = models.DateField(null=True, blank=True)
    start_date = models.DateField( null=True, blank=True)
    end_date = models.DateField( null=True, blank=True)

    def __str__(self):
        return self.employee_name

