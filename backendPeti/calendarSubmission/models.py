from django.db import models

class CalendarSubmission(models.Model):
    title_day = models.CharField( max_length=220, null=True, blank=False)
    type_day = models.CharField( max_length=220, null=True, blank=True)
    date = models.DateField( null=True, blank=False)
    years = models.IntegerField( null=True, blank=True)
    months = models.IntegerField( null=True, blank=True)
    days = models.IntegerField( null=True, blank=True)
    day_of = models.CharField( max_length=220, null=True, blank=True)
    day_names = models.CharField(max_length=240, null=True, blank=True)
    day_opti = models.CharField(max_length=240, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.years = (self.date.year)
        self.months = (self.date.month)
        self.days = (self.date.day)
        if(self.date != None):
            dates = (self.date.strftime('%A'))
            self.day_names = dates
        super(CalendarSubmission, self).save(*args, **kwargs)
 
    def __str__(self):  
        return self.title_day