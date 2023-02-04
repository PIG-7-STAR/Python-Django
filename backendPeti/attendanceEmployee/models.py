from django.db import models

class AttendanceEmployee(models.Model):
    employee_name = models.CharField( max_length=220, null=True, blank=False)
    working_date = models.DateField( null=True, blank=True)
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
            if(finn > '59'):
                ef = self.end_from-100+60
                self.working_hour = (ef - self.start_from)
                self.working_hour_detail = self.working_hour/100
            elif(tle > 1 ):
                if(finn > '59'):
                    self.working_hour = calc-40
                    self.working_hour_detail = self.working_hour/100
                else:
                    self.working_hour = calc-40
                    self.working_hour_detail = self.working_hour/100     
            elif(tle == 2 ):
                self.working_hour = calc-40
                self.working_hour_detail = self.working_hour/100
            else:
                self.working_hour = calc
                self.working_hour_detail = calc/100
        if(self.lembur_start != None and self.lembur_start != None):
            calc_lembur = (self.lembur_end - self.lembur_start)
            tlembur = len(str(calc_lembur))
            if(tlembur == 1):
                tawLembur = tlembur
            elif(tlembur > 1):
                tawLembur = tlembur-2
            slicesLembur = slice(tawLembur,tlembur)
            dig_lembur = str(calc_lembur)
            finn_lembur = dig_lembur[slicesLembur]
            if(finn_lembur > '59'):
                ef_lembur = self.lembur_end-100+60
                self.lembur_hour = (ef_lembur - self.lembur_start)
            elif(tlembur > 1 ):
                if(finn_lembur > '59'):
                    self.lembur_hour = calc_lembur-40
                else:
                    self.lembur_hour = calc_lembur-40
            elif(tlembur == 2 ):
                self.lembur_hour = calc_lembur-40
            else:
                self.lembur_hour = calc_lembur
        # if(self.lembur_hour != None):
        #     self.working_hour_total = (self.working_hour + self.lembur_hour)
        # else:
        #     self.working_hour_total = (self.working_hour + 0)

        self.years = (self.working_date.year)
        self.months = (self.working_date.month)
        super(AttendanceEmployee, self).save(*args, **kwargs)
 
    def __str__(self):  
        return self.employee_name

class PercentageAttendanceEmployee(models.Model):
    name_label = models.CharField(max_length=245, null=True, blank=False)
    total_employee_active = models.IntegerField( null=True, blank=True)
    total_working_days = models.IntegerField( null=True, blank=True)
    percentage = models.CharField( max_length=245, null=True, blank=True)

    def save(self, *args, **kwargs):
        wk_hour = ((self.total_employee_active * 800) * self.total_working_days)
        wd_hour = ((self.total_working_days * 800) * self.total_employee_active)
        self.percentage = ( (wk_hour / wd_hour) * 100)
        super(PercentageAttendanceEmployee, self).save(*args, **kwargs)
    
    def __str__(self):  
        return self.name_label