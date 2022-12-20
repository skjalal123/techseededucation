from django.contrib import admin
from .models import Cart


# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'status']
    readonly_fields = ['course', 'student', 'status']

