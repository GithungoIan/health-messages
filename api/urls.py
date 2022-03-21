from django.urls import path

from accounts.views import DepartmentView, PatientView
from api.views import AppointmentView

urlpatterns = [
    path('appointments/', AppointmentView.as_view()),
    path('departments/', DepartmentView.as_view()),
    path('patients/', PatientView.as_view()),
]
