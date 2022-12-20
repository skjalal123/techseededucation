from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *


# Register your models here.
class Qualification(admin.StackedInline):
    model = qualification


class Achievement(admin.StackedInline):
    model = achievement


class Experiences(admin.StackedInline):
    model = Experience


@admin.register(myUser, )
class UserPanel(UserAdmin):
    model = myUser
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('profile', 'email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'mobile', 'is_student', 'is_teacher', 'date_of_birth', 'interest', 'hobby')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'profile', 'full_name', 'mobile', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('date_joined',)
    required = ('first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [Qualification, Achievement, Experiences]


@admin.register(OneTimePassword)
class Otp(admin.ModelAdmin):
    list_display = ['profileId', 'One_Time_Password', 'expiryDate']
    readonly_fields = ['profileId', 'One_Time_Password', 'expiryDate']
    search_fields = ['profileId']
    ordering = ['-expiryDate']

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
