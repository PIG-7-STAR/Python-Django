from rest_framework import serializers
from pengajuanEmp.models import Petitions, PetitionsCalendar

class PetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petitions
        fields = '__all__' 

class PetitionsCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetitionsCalendar
        fields = '__all__' 
        
        