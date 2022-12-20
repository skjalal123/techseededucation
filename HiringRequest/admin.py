from django.contrib import admin
from .models import HiringRequest, EnquiryRequest, Feedback


# Register your models here.


@admin.register(HiringRequest)
class HiringRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation', 'company', 'position']


@admin.register(EnquiryRequest)
class EnquiryRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']
