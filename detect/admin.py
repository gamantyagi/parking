from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import details, ImageOb


class detailsInline(admin.StackedInline):
    model = details
    can_delete = False
    verbose_name_plural = 'details'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (detailsInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ImageOb)
