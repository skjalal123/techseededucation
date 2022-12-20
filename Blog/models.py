from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid


class BlogType(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Blog(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    slug = models.CharField(max_length=255,help_text="max 255 characters are allowed", blank=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.SET_NULL,null=True)
    blog_title = models.CharField(max_length=255,help_text="max 255 characters are allowed")
    thumbnail = models.FileField(upload_to="blogs/", help_text="Thumbnail for you post")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_title)
        super(Blog, self).save(*args, **kwargs)
