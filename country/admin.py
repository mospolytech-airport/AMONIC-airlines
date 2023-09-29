from django.contrib import admin
from country.models import Country
# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'country_id')
    list_display_links = ('id','name')
    search_fields = ('id', 'name','country_id',)

admin.site.register(Country, CountryAdmin)