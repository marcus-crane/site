from django.contrib import admin
from django.utils import timezone

from .models import Post

def publish(modeladmin, request, queryset):
    queryset.update(status='P', date=timezone.now())
publish.short_description="Publish posts"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status')
    list_filter = ['date', 'status']
    search_fields = ['title']
    actions = [publish]

admin.site.register(Post, PostAdmin)
