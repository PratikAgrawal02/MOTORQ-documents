from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Document 
from .serializers import UserSerializer , UserLoginSerializer ,DocumentSerializer
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.contrib.auth.models import User
from  rest_framework.authentication import TokenAuthentication


from rest_framework.decorators import permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token  
from drf_yasg.utils import swagger_auto_schema
@swagger_auto_schema(
    method='post',
)

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
            phoneNumber = serializer.validated_data['phoneNumber']
            password = serializer.validated_data['password']

            user = authenticate(request, username=phoneNumber, password=password)

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
        phone_number=[user.username for user in users]
        return Response({'phone_numbers': phone_number})
    
    
class DocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data, context={'request': request})  # Pass 'request' to the serializer context
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        documents = Document.objects.filter(owner=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, document_id):
        try:
            return Document.objects.get(id=document_id, owner=self.request.user)
        except Document.DoesNotExist:
            raise Http404
    def get(self, request, document_id, format=None):
        document = self.get_object(document_id)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    def delete(self, request, document_id, format=None):
        document = self.get_object(document_id)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DocumentSharingView(APIView):
    def get_document(self, document_id):
        try:
            return Document.objects.get(id=document_id, owner=self.request.user)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, document_id, format=None):
        document = self.get_document(document_id)
        shared_users = document.shared_with.all().exclude(username=request.user.username)
        shared_phone_numbers = [user.username for user in shared_users]
        return Response({'shared_phone_numbers': shared_phone_numbers})

    def post(self, request, document_id, format=None):
        document = self.get_document(document_id)
        shared_phone_numbers = request.data.get('shared_phone_numbers', [])

        # Validate and process shared phone numbers
        shared_users = []
        for phone_number in shared_phone_numbers:
            try:
                user = User.objects.get(username=phone_number)
                shared_users.append(user)
            except User.DoesNotExist:
                return Response({'message': f'User with phone number {phone_number} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Clear existing shared users and set the new ones
        document.shared_with.clear()
        document.shared_with.add(*shared_users)

        return Response({'message': 'Document sharing updated successfully.'}, status=status.HTTP_200_OK)

class SharedDocumentsListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get_queryset(self):
        return Document.objects.filter(shared_with=self.request.user)