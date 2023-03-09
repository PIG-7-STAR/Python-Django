from rest_framework import serializers
from submisssion.models import Submission, CalendarCutiSubmission
from userapp.serializer import UserDetailsSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    employee_id = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'employee_id',
            'employee_name',
            'division',
            'permission_type',
            'reason',
            'start_date',
            'end_date',
            'jumlah_hari',
            'from_hour',
            'end_hour',
            'lembur_hour',
            'return_date',
            'permission_pil',
            'reason_rejected',
            'conditional_reasons',
            'suspended_start',
            'suspended_end',
            'created_at',
            'updated_at'
        ]
        depth = 1

class SubmissionCutiCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarCutiSubmission
        fields = '__all__' 
        