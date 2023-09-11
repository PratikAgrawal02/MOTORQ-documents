from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer , UserLoginSerializer , UserListSerializer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token  

class UserSignupView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            password = serializer.validated_data['password']

            user = authenticate(request, username=mobile_number, password=password)

            if user is not None:
                login(request, user)

                # Generate or retrieve a token for the user
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)