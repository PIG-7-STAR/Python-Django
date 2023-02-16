from django.db import models


class CalendarDashHRD(models.Model):
    title_day = models.CharField( max_length=220, null=True, blank=False)
    type_day = models.CharField( max_length=220, null=True, blank=True)
    date = models.DateField( null=True, blank=False)
    years = models.IntegerField( null=True, blank=True)
    months = models.IntegerField( null=True, blank=True)
    days = models.IntegerField( null=True, blank=True)
    day_of = models.CharField( max_length=220, null=True, blank=True)
    day_name = models.CharField(max_length=240, null=True, blank=True)
    day_opt = models.CharField(max_length=240, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.years = (self.date.year)
        self.months = (self.date.month)
        self.days = (self.date.day)
        if(self.date != None):
            dates = (self.date.strftime('%A'))
            self.day_name = dates
        super(CalendarDashHRD, self).save(*args, **kwargs)
 
    def __str__(self):  
        return self.title_day

class DashboardHRD(models.Model):
    total_days = models.IntegerField( null=True, blank=False)
    total_employee = models.IntegerField( null=True, blank=False)
    hour_perday = models.IntegerField( null=True, blank=False)
    total_hour = models.CharField( max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        t_day = self.total_days
        t_emp = self.total_employee
        hd = self.hour_perday
        self.total_hour = (t_emp * hd) * t_day
        super(DashboardHRD, self).save(*args, **kwargs)
 
    def __str__(self):  
        return self.total_days