from django.contrib import admin
from memberships.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'club', 'role', 'status', 'created_at']
    list_filter = ['role', 'status', 'created_at']
    search_fields = ['user__username', 'club__name']
    list_editable = ['role', 'status']
    readonly_fields = ['created_at', 'updated_at']