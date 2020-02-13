from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreateAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'is_active']
    list_filter = ['is_active']
    ordering = ['id']
    search_fields = ['email', 'name']
    add_form = UserCreateAdminForm
    add_fieldsets = (
        ('계정정보', {'fields': [
            'email',
            'password1',
            'password2'
        ]}),
        ('개인정보', {'fields': [
            'name'
        ]}),
    )
    fieldsets = [
        ('계정정보', {'fields': [
            'email',
            'password'
        ]}),
        ('개인정보', {'fields': [
            'name'
        ]}),
        ('권한', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
        )})
    ]
