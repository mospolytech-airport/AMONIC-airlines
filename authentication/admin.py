from django.contrib import admin
from authentication.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'first_name','last_name', 'birthday',)
    list_display_links = ('id','email','first_name','last_name','birthday')
    search_fields = ('id', 'email','last_name',)
    list_filter = ('last_name', 'email')

admin.site.register(User, UserAdmin)