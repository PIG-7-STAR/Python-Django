from rest_framework import serializers
from fistApp.models import Pengajuans

class PengajuansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuans
        fields = '__all__' 