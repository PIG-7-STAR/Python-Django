from rest_framework import serializers
from pengajuanEmp.models import Petitions

class PetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petitions
        fields = '__all__' 
        