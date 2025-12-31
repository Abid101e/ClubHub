from django.contrib import admin
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'author', 'type', 'is_published', 'created_at']
    list_filter = ['type', 'is_published', 'created_at', 'club']
    search_fields = ['title', 'body', 'author__username', 'club__name']
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']