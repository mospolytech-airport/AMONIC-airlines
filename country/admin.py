from django.contrib import admin
from country.models import Country
# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('id', 'name')

admin.site.register(Country, CountryAdmin)