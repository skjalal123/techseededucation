from django.contrib import admin
from .models import *


# Register your models here.


class Options(admin.StackedInline):
    model = Option


@admin.register(Subject)
class Subjects(admin.ModelAdmin):
    list_display = ['course', 'Subject_Name', 'thumbnail']


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['questions', 'images']
    inlines = [Options, ]


@admin.register(Option)
class option(admin.ModelAdmin):
    list_display = ['Question', 'option']
