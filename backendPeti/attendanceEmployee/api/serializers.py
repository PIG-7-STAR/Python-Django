from rest_framework import serializers
from attendanceEmployee.models import AttendanceEmployee, PercentageAttendanceEmployee

class AttendanceEmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttendanceEmployee
        fields = '__all__' 

class PercentageAttendanceEmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PercentageAttendanceEmployee
        fields = '__all__' 
