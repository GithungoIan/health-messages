from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.models import Department, PatientGroup


class Base(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class AppointmentType(models.TextChoices):
    CHECKUP = 'checkup', _('Checkup')
    EMERGENCY = 'emergency', _('Emergency')
    FOLLOW_UP = 'follow_up', _('Follow Up')
    ROUTINE = 'routine', _('Routine')
    WALK_IN = 'walk_in', _('Walk In')


class Appointment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=AppointmentType.choices)
    description = models.TextField()
    notified = models.BooleanField(default=False)
    reminded = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    date_visited = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class BroadcastMessage(models.Model):
    group = models.CharField(max_length=100, choices=PatientGroup.choices, null=True, blank=True)
    facilities = models.BooleanField(default=False)
    message = models.TextField()
    completed = models.BooleanField(default=False)
    phones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.message

