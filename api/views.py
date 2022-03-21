from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Department
from api.models import Appointment
from api.serializers import AppointmentSerializer


class AppointmentView(APIView):

    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():

            _dept = data['department']
            department = Department.objects.filter(Q(pk=_dept) | Q(name=_dept))
            error = 0
            msg = ""
            if department.exists():
                data["department_id"] = department.first().pk
            else:
                error = 1
                msg = "Invalid Department Value"

            # _usr = data["user"]
            # user = User.objects.filter(Q(pk=_usr) | Q(username=_usr))
            # if user.exists():
            #     data["user"] = user.first().pk
            # else:
            #     error = 1
            #     msg = "Invalid User Value"
            #
            if error == 1:
                return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)
            _ser = AppointmentSerializer(data=data)
            if _ser.is_valid():
                _ser.save()
                return Response(data=_ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=_ser.errors, status=status.HTTP_400_BAD_REQUEST)

            # serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
