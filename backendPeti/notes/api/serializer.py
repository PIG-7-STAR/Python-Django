from rest_framework import serializers
from notes.models import NotesHrd, EmployeeCuti
from userapp.models import User

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesHrd
        fields = '__all__'
        # exclude = ['type_notes']
        # depth = 1

class EmployeeCutiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCuti
        fields = '__all__' 
        depth = 1
        