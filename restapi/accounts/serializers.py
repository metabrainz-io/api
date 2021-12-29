from rest_framework import serializers
from accounts.models import UserAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"

from django.contrib.auth import get_user_model

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'c_addr')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['c_addr'] = user.c_addr
        print(user.c_addr)
        return token

    def get_user_token(self, user):
        refresh = RefreshToken.for_user(user)

        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }