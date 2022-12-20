from django.contrib import admin
from .models import Blog, BlogType
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content']
    readonly_fields = ['created_at']
    list_display = ['blog_title']

admin.site.register(BlogType)