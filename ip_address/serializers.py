
from rest_framework import serializers
from ip_address.models import IpAddress

class IpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = '__all__'