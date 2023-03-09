from rest_framework import serializers
from noteHR.models import NotesApp
from userapp.serializer import UserDetailsSerializer
# from userapp.models import User
class NotesSerializer(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = NotesApp
        fields = [
                    'id', 
                    'employee', 
                    'date_note', 
                    'name_day', 
                    'notes', 
                    'type_notes', 
                    'hari', 
                    'bulan', 
                    'tahun', 
                    'created_at', 
                    'updated_at'
                ]
        depth = 1

