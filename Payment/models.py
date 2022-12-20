from django.db import models
import uuid
from django.utils import timezone


# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)

    course = models.ForeignKey('Course.Course', on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey('Profile.myUser', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=25, blank=True)
    added_to_cart = models.DateTimeField(default=timezone.now)
    confirm = models.DateTimeField(default= timezone.now, blank=True)

    def __str__(self):
        return f"{self.course.course_title} from {self.student.email}"

