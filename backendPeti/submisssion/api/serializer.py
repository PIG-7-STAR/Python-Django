from rest_framework import serializers
from submisssion.models import Submission, CalendarCutiSubmission
from userapp.serializer import UserDetailsSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'employee',
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
            'status_submission',
            'created_at',
            'updated_at'
        ]
        depth = 1

class SubmissionEmployeeSerializer(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'employee',
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
            'status_submission',
            'created_at',
            'updated_at'
        ]

class SubmissionCutiCalendarSerializer(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = CalendarCutiSubmission
        fields = [
            "id",
            "title",
            "permission_type",
            "reason",
            "start",
            "end",
            "color",
            "employee",
        ]
        