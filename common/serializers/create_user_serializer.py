from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_username(self, username):
        is_exist = UserModel.objects.filter(username=username).exists()
        if is_exist:
            raise ValidationError('Username already exists')
        return username
