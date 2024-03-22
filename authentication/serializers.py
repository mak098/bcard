from rest_framework import serializers
from .models import User
from Agency.serializers import AgencySerializer

class UserSerializer (serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    class Meta:
        model = User
        fields= ('agency','username', 'email', 'first_name', 'last_name','auth_token')