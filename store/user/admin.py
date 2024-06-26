from django.contrib import admin

from store.user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login',
                    'is_active', 'is_superuser', 'is_staff', 'public_id')
    search_fields = ('email', 'first_name', 'last_name',)