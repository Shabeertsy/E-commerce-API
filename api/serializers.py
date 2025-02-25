from rest_framework import serializers

from rest_framework import serializers
from . models import FarmerRegistration,Profile,Notice,OfficerRegistration,Query

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerRegistration
        fields = '__all__'

class FarmerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerRegistration
        fields = '__all__'


class FarmerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerRegistration
        fields = '__all__'
        depth=1


class OfficerListSerializer(serializers.ModelSerializer):
    class Meta:
         model=OfficerRegistration
         fields='__all__'
         depth=1


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = 'all'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField(write_only=True)

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notice
        fields='__all__'
    
class OfficerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
         model=OfficerRegistration
         fields='all'


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model=Query
        fields='all'

class ListQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model=Query
        fields='all'
        depth=1