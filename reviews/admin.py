from django.contrib import admin
from django.utils import timezone

from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ['date']
    search_fields = ['title']

admin.site.register(Review, ReviewAdmin)
