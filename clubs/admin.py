from django.contrib import admin
from clubs.models import Club


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'created_at', 'get_member_count']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}

    def get_member_count(self, obj):
        return obj.membership_set.filter(status='APPROVED').count()
    get_member_count.short_description = 'Members'