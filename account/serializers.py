from rest_framework import serializers
from .models import UserAccount
import re


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username is required")
        if UserAccount.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address")
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        strong_password_regex = (
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])'
            r'[A-Za-z\d@$!%*?&#]{8,}$')

        if not re.match(strong_password_regex, value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters"
                "include uppercase cand special character")
        return value

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields=['username', 'password']
        extra_kwargs={'password':{'write_only': True}}

class Userserail(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields = ["id", "username", "email", "role", "status",'is_email_verified']