from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    #მომხმარებლის ადმინ პანელში მართვა

    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_active_member', 'date_joined'
    ]

    list_filter = ['role', 'is_active_member', 'is_staff', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    ordering = ['-date_joined']
    list_display_links = ['username', 'email']
    list_editable = ['is_active_member']
    list_per_page = 25

    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('username', 'password', 'email')
        }),
        ('პერსონალური ინფორმაცია', {
            'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'address', 'profile_image')
        }),
        ('როლები და უფლებები', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('საწევროს ინფორმაცია', {
            'fields': ('is_active_member', 'membership_start')
        }),
        ('მნიშვნელოვანი თარიღები', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login', 'membership_start']

#პაროლის აღდგენის ტოკენები
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):

    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['user', 'token', 'created_at', 'expires_at']
    ordering = ['-created_at']
    list_per_page = 25

    def has_add_permission(self, request):
        return False