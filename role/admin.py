from django.contrib import admin
from role.models import Role
# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'role_id')
    list_display_links = ('id','title', 'role_id')
    search_fields = ('id','title', 'role_id')

admin.site.register(Role, RoleAdmin)
