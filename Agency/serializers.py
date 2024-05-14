from rest_framework import serializers
from .models import Firm,Agency, LiasonAgency,InterrestRateConfig

class FirmSerializer (serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields= ('name','id','email','phone', 'address','logo')

class AgencySerializer (serializers.ModelSerializer):
    firm = FirmSerializer(read_only= True)
    class Meta:
        model = Agency
        fields= ('firm','id','name', 'address','phone','email')

class Agency_Serializer (serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields= ('id','name', 'address','phone')

class LiasonAgencySerializer (serializers.ModelSerializer):
    origin = Agency_Serializer(read_only= True)
    destination = Agency_Serializer(read_only= True)
    class Meta:
        model = LiasonAgency
        fields= ('origin','destination','id')

class InterrestRateConfigSerializer (serializers.ModelSerializer):
    agency_liason = LiasonAgencySerializer(read_only= True)
    class Meta:
        model = InterrestRateConfig
        fields = ('agency_liason','id','rate', 'forfait','threshold','status')
