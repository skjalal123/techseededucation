from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from Course.models import Course
from django.core.mail import EmailMultiAlternatives
import uuid
from django.conf import settings
import random

# Create your models here.

types = [('Student', 'Student'),
         ('Author', 'Author')]


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        self.email_user("Activate Account", email)
        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

    @staticmethod
    def email_user(subject, to):
        """Send an email to this user."""
        text_content = 'This is an important message.'
        html_content = '<p>Congratulations! your account has created successfully please click on the below link to activate the account</p>'
        msg = EmailMultiAlternatives(subject, text_content, 'info@techseededucation.com', [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class myUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    profile = models.FileField(
        verbose_name="Profile",
        upload_to="profile",
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=20, blank=True,
                                  null=True)
    last_name = models.CharField(max_length=20, blank=True,
                                 null=True)
    Type = models.CharField(
        verbose_name="Type",
        max_length=8,
        choices=types,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True
    )
    mobile = models.CharField(
        verbose_name="Mobile",
        max_length=13,
        blank=True,
        null=True
    )
    city = models.CharField(
        verbose_name="City",
        max_length=25,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        blank=True,
        null=True
    )
    interest = models.CharField(
        verbose_name="Interest",
        max_length=10,
        blank=True,
        null=True
    )
    hobby = models.CharField(
        verbose_name="Hobby",
        max_length=100,
        blank=True,
        null=True
    )
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    seed_coin = models.IntegerField(default=0)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'My User'
        verbose_name_plural = 'My Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class qualification(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_qualification',
                                   on_delete=models.CASCADE)
    Degree = models.CharField(max_length=100)
    passing_year = models.DateField()
    institute = models.CharField(max_length=200)
    percentage = models.FloatField(default=0)


class achievement(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_achievement',
                                   on_delete=models.CASCADE)
    certificate = models.CharField(max_length=200)
    description = models.TextField()


class Experience(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_experience',
                                   on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    duration = models.DurationField()
    description = models.TextField()


def setExpiryDateTimeForOTP():
    return timezone.now() + timezone.timedelta(minutes=15)


class OneTimePassword(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    profileId = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_otp', on_delete=models.CASCADE)
    One_Time_Password = models.IntegerField(unique=True, blank=True)
    expiryDate = models.DateTimeField(default=setExpiryDateTimeForOTP)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        otp = random.randint(100001, 999999)
        self.One_Time_Password = otp
        super(OneTimePassword, self).save(*args, **kwargs)
