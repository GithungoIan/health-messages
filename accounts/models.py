from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    PATIENT = 'patient'
    DOCTOR = 'doctor'


class PatientGroup(models.TextChoices):
    HIV_AIDS = 'hiv_aids', _('HIV / AIDS Group')
    CANCER = 'cancer', _('Cancer Group')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=Role.choices)
    group = models.CharField(max_length=100, choices=PatientGroup.choices, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
