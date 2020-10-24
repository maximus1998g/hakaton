from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .serializers import *
from .models import UserProfile
from .enums import Type
from company.serializers import CompanySerializer
from company.models import Company


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
            if not user:
                raise Http404
            token, _ = Token.objects.get_or_create(user=user)

            response = dict({})
            response['token'] = token.key
            response['type'] = request.data.get('type')

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthCredentialsSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(email=email, password=password)
        if not user:
            raise Http404
        token, _ = Token.objects.get_or_create(user=user)

        response = dict({})
        response['token'] = token.key
        response['type'] = UserProfile.objects.get(email=email).type

        return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        serializer = None

        if self.request.user.type == Type.EMPLOYER.value:
            company = Company.objects.filter(hr=self.request.user)
            if not company:
                return Response({'error': 'user does not have any companies'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CompanySerializer(company[0])

        elif self.request.user.type == Type.STUDENT.value:
            serializer = UserProfileSerializer(self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)