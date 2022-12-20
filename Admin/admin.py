from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.


@admin.register(TermOfUser)
class TermOfUse(SummernoteModelAdmin):
    summernote_fields = ['description']
    list_display = ['title']


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(SummernoteModelAdmin):
    summernote_fields = ['description']
    list_display = ['questions']


@admin.register(Founder)
class FoundersAdmin(SummernoteModelAdmin):
    list_display = ['name', 'position', 'education', 'contact']
