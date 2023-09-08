from django.db import models
from userapp.models import User
# import locale
from datetime import datetime

class PresenceEmployee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='working_hours')
    working_date = models.DateField( null=False, blank=False)
    start_from = models.IntegerField( null=True, blank=True)
    end_from = models.IntegerField( null=True, blank=True)
    lembur_start = models.IntegerField( null=True, blank=True)
    lembur_end = models.IntegerField( null=True, blank=True)
    working_hour = models.IntegerField( null=True, blank=True)
    lembur_hour = models.IntegerField( null=True, blank=True)
    working_hour_total =  models.IntegerField( null=True, blank=True)
    working_hour_detail = models.FloatField( null=True, blank=True)
    lembur_hour_detail = models.FloatField( null=True, blank=True)
    years = models.IntegerField( null=True, blank=True)
    months = models.IntegerField( null=True, blank=True)
    days = models.CharField( max_length=220, null=True, blank=True)
    ket = models.CharField( max_length=255, null=True, blank=True)
    is_lock = models.BooleanField( default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if(self.end_from != None and self.start_from != None):
            calc = (self.end_from - self.start_from)
            tle = len(str(calc))
            if(tle == 1):
                taw = tle
            elif(tle > 1):
                taw = tle-2
            slic = slice(taw,tle)
            dig = str(calc)
            finn = dig[slic]

            lenstart = len(str(self.start_from))
            lenend = len(str(self.end_from))
            tlestr = lenstart-2
            tleend = lenend-2

            slicstr = slice(tlestr,lenstart)
            digstr = str(self.start_from)
            finnstr = digstr[slicstr]

            slicend = slice(tleend,lenend)
            digend = str(self.end_from)
            finnend = digend[slicend]

            if(finn > '59'):
                ef = self.end_from-100+60
                self.working_hour = (ef - self.start_from)
                self.lembur_hour_detail = self.working_hour/100
            elif(tle > 1 ):
                if(finn > '59'):
                    self.working_hour = calc-100+60
                    self.lembur_hour_detail = self.working_hour/100
                # elif(finn == '00'):
                #     self.working_hour = calc-100+60
                #     self.lembur_hour_detail = self.working_hour/100
                elif(finn < '60'):
                    if(finnend < finnstr):
                        self.working_hour = calc-40
                        self.lembur_hour_detail = self.working_hour/100
                    else: 
                        self.working_hour = calc
                        self.lembur_hour_detail = self.working_hour/100
                else:
                    self.working_hour = calc-40
                    self.lembur_hour_detail = self.working_hour/100
            elif(tle == 2 ):
                self.working_hour = calc-100+60
                self.lembur_hour_detail = self.working_hour/100
            else:
                self.working_hour = calc
                self.lembur_hour_detail = calc/100

        
        if(self.lembur_end != None and self.lembur_start != None):
            calclembur = (self.lembur_end - self.lembur_start)
            tleLembur = len(str(calclembur))
            if(tleLembur == 1):
                tawLembur = tleLembur
            elif(tleLembur > 1):
                tawLembur = tleLembur-2
            slicLembur = slice(tawLembur,tleLembur)
            digLembur = str(calclembur)
            finn = digLembur[slicLembur]

            lemburstart = len(str(self.lembur_start))
            lemburend = len(str(self.lembur_end))
            lemstr = lemburstart-2
            lemend = lemburend-2

            lemburslicstr = slice(lemstr,lemburstart)
            lemburdigstr = str(self.lembur_start)
            lemburfinnstr = lemburdigstr[lemburslicstr]

            lemburslicend = slice(lemend,lemburend)
            lemburdigend = str(self.lembur_end)
            lemburfinnend = lemburdigend[lemburslicend]

            if(finn > '59'):
                lemburef = self.lembur_end-100+60
                self.lembur_hour = (lemburef - self.lembur_start)
                self.working_hour_detail = self.lembur_hour/100
            elif(tleLembur > 1 ):
                if(finn > '59'):
                    self.lembur_hour = calclembur-100+60
                    self.working_hour_detail = self.lembur_hour/100
                # elif(finn == '00'):
                #     self.lembur_hour = calclembur-100+60
                #     self.working_hour_detail = self.lembur_hour/100
                elif(finn < '60'):
                    if(lemburfinnend < lemburfinnstr):
                        self.lembur_hour = calclembur-40
                        self.working_hour_detail = self.lembur_hour/100
                    else: 
                        self.lembur_hour = calclembur
                        self.working_hour_detail = self.lembur_hour/100
                else:
                    self.lembur_hour = calclembur-40
                    self.working_hour_detail = self.lembur_hour/100
            elif(tleLembur == 2 ):
                self.lembur_hour = calclembur-100+60
                self.working_hour_detail = self.lembur_hour/100
            else:
                self.lembur_hour = calclembur
                self.working_hour_detail = calclembur/100
        
        if(self.working_date != None):
            work_date = self.working_date
            self.days = work_date.strftime('%A')
            self.years = work_date.strftime('%Y')
            self.months = work_date.strftime('%m')
        super(PresenceEmployee, self).save(*args, **kwargs)
 
    def __str__(self):  
        return self.employee.name