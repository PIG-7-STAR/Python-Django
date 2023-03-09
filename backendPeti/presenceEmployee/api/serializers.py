from rest_framework import serializers
from attendanceEmployee.models import AttendanceEmployee
from userapp.serializer import UserDetailsSerializer

class PresenceEmployeeSerializers(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = AttendanceEmployee
        fields = ['id', 'employee', 'working_date', 'start_from', 'end_from','working_hour',
                  'lembur_start', 'lembur_end','lembur_hour', 'years', 'months', 'days', 'ket']
    