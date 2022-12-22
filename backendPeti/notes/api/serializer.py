from rest_framework import serializers
from notes.models import NotesHrd

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesHrd
        fields = '__all__' 
        