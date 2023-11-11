from import_export import resources, formats
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from role.models import Role
from schedules.models import Schedule

class ScheduleResource(resources.ModelResource):
    class Meta:
        model = Schedule

class ScheduleAdmin(ImportExportModelAdmin):
    resource_classes = [ScheduleResource]
    formats = [base_formats.XLSX]

admin.site.register(Schedule, ScheduleAdmin)