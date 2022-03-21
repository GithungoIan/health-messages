from django.contrib import admin

from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'group', )


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department)
admin.site.register(Facility, FacilityAdmin)
