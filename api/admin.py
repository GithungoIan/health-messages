from django.contrib import admin

from .models import *


class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('user', 'date', 'type', 'visited', 'notified', 'reminded')
    list_filter = ('type', 'visited', 'notified', 'reminded')
    search_fields = ('user__username',)


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(BroadcastMessage)
