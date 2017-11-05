from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status')
    list_filter = ['date', 'status']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
