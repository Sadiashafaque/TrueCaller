from rest_framework.views import APIView
from SpamCaller.models.models import RegisteredProfile
from SpamCaller.serializers import RegisteredProfileSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny



class RegisterProfileView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny,]
    def post(self, request):
        serialized = RegisteredProfileSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny,]
    def post(self,request):
        if request.method == 'POST':
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                login(request, user)
                token, created = Token.objects.get_or_create(user = user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        
