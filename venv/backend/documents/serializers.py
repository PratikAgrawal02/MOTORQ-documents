from rest_framework import serializers
from .models import  Document
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import Http404

import re 

class UserSerializer(serializers.Serializer):
    phoneNumber=serializers.CharField(validators=[
        validators.RegexValidator(
            regex='^\d{10}$',
            message='Mobile number must be 10 digits long.',
            code='invalid_mobile_number'
        ),
    ])
    password=serializers.CharField()

    def validate(self,data):
        if data['phoneNumber']:
            if User.objects.filter(username=data['phoneNumber']).exists():
                raise serializers.ValidationError("phone number already exists")
            
        return data
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isalpha() for char in value) or \
           not any(char.isdigit() for char in value) or \
           not any(char in "!@#$%^&*()_-+=<>?/[]{}" for char in value):
            raise ValidationError("Password must contain at least one alphabet, one number, and one special character.")

        return value

    def create(self, validated_data):
        user=User.objects.create_user(username=validated_data['phoneNumber'], password=validated_data['password'])
        user.save()

        return validated_data

class UserLoginSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=128, write_only=True)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name','owner', 'shared_with']

    def create(self, validated_data):
        user = self.context['request'].user

        document = Document.objects.create(owner=user, **validated_data)
        return document
    