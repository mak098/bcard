from rest_framework import serializers
from .models import CashIn,CashOut
from Agency.serializers import InterrestRateConfigSerializer
from authentication.serializers import PUserSerializer

class CashInSerializer(serializers.ModelSerializer):
    interrest_config = InterrestRateConfigSerializer(read_only=True)
    created_by = PUserSerializer(read_only=True)
    class Meta:
        model = CashIn
        fields = ('url','interrest_config','created_by',"code","sender","sender_phone","sender_id_or_passport","amount","distribution","recipient","recipient_phone","recipient_id_or_passport","comment","status","created_at")
        
class CashOutSerializer(serializers.ModelSerializer):
    cash_in =CashInSerializer(read_only =True)
    created_by = PUserSerializer(read_only=True)
    
    class Meta:
        model = CashOut
        fields = ("cash_in",'created_by',"amount","recipient","recipient_phone","recipient_id_or_passport","comment","created_at")
