from django.contrib import admin
from role.models import Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('id','title')

admin.site.register(Role, RoleAdmin)
