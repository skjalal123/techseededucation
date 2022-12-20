from django.contrib import admin
from django_summernote.admin import SummernoteInlineModelAdmin, SummernoteModelAdmin
from .models import *

# Register your models here.

admin.site.register(CourseList)


class VideoInline(admin.StackedInline):
    model = Video
    readonly_fields = ['updatedAt']
    ordering = ['updatedAt']
  

class Lessons(admin.StackedInline):
    model = Lesson
    list_display = ['courses', 'Lesson_Name']
    readonly_fields = ['updatedAt']
    ordering = ['-updatedAt']


@admin.register(Video)
class Display(admin.ModelAdmin):
    list_display = ['title', 'time']
    readonly_fields = ['updatedAt']
    ordering = ['time']


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    list_display = ['course_title', 'course_type_detail']
    summernote_fields = ['course_description']
    readonly_fields = ['updatedAt']
    empty_value_display = 'blank'
    ordering = ["-updatedAt"]
    # date_hierarchy = 'updatedAt'
    inlines = [
        Lessons,
    ]


@admin.register(Question)
class Questions(admin.ModelAdmin):
    list_display = ['student', 'author', 'question_title', 'question_time']
    readonly_fields = ['question_time']


@admin.register(Answer)
class Answers(admin.ModelAdmin):
    list_display = ['author', 'answer', 'reply_time']
    readonly_fields = ['reply_time']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['Lesson_Name','updatedAt']
    ordering = ["-updatedAt"]
    inlines = [
        VideoInline,
    ]


@admin.register(Comment)
class Comments(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', ]


@admin.register(Note)
class Note(admin.ModelAdmin):
    list_display = ['by', 'timestamp', 'updatedAt']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
