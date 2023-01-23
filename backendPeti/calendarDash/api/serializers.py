from rest_framework import serializers
from calendarDash.models import CalendarDashHRD, DashboardHRD

class CalendarDashSerializers(serializers.ModelSerializer):
    class Meta:
        model = CalendarDashHRD
        fields = '__all__' 

class DashboardHrdSerializers(serializers.ModelSerializer):
    class Meta:
        model = DashboardHRD
        fields = '__all__' 
