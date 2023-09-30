from django.contrib import admin
from office.models import Office
# Register your models here.
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id','title','country_id', 'phone','contact')
    list_display_links = ('id','title', 'phone',)
    search_fields = ('id','title', 'phone','contact')

admin.site.register(Office, OfficeAdmin)