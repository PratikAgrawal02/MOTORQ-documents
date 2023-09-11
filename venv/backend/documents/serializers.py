from rest_framework import serializers
from .models import Person , Document
import re  # Import Python's regular expression module

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'mobile_number', 'password']

    def validate_mobile_number(self, value):
        # Check if mobile_number is 10 digits
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Mobile number must be 10 digits.")
        
        # Check if the mobile_number is unique
        if Person.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already in use.")
        
        return value

    def validate_password(self, value):
        # Check if password is at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Check if password contains at least one alphabet, one number, and one special character
        if not any(char.isalpha() for char in value) or \
           not any(char.isdigit() for char in value) or \
           not any(char in "!@#$%^&*()_+{}[];:'\"<>,.?/" for char in value):
            raise serializers.ValidationError("Password must contain at least one alphabet, one number, and one special character.")
        
        return value

class UserLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=128, write_only=True)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['mobile_number']
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name']

    def create(self, validated_data):
        # Get the authenticated user from the request context
        user = self.context['request'].user

        # Create a new document with the owner set to the authenticated user
        document = Document.objects.create(owner=user, **validated_data)
        return document