from django.contrib import admin
from django.utils import timezone

from .models import Post

def publish(modeladmin, request, queryset):
    queryset.update(status='P', published_at=timezone.now(), last_modified=timezone.now())
    publish.short_description="Publish posts"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'status')
    list_filter = ['published_at', 'status']
    search_fields = ['title', 'status']
    actions = [publish]

admin.site.register(Post, PostAdmin)
