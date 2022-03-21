from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, Role, Department
from accounts.serializers import UserSerializer
from api.serializers import DepartmentSerializer


class DepartmentView(APIView):

    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PatientView(APIView):

    def get(self, request, format=None):
        patients = User.objects.filter(profile__role=Role.PATIENT)
        serializer = UserSerializer(patients, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
