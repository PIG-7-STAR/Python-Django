from rest_framework import serializers
from saldoCuti.models import SaldoCuti

class SaldoCutiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaldoCuti
        fields = '__all__' 
        