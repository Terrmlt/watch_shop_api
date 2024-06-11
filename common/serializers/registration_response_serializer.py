from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class RegistrationResponseSerializer(serializers.ModelSerializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'access', 'refresh')
