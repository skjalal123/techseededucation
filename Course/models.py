import uuid

import enum
from django.conf import settings
from django.db import models
from django.utils import timezone


def user(request):
    current_user = request.user
    return current_user.id


class CourseList(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    CourseList = models.CharField(max_length=50, unique=True)
    updatedAt = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.CourseList


class Course(models.Model):
    id = models.AutoField(primary_key=True, 
        editable=False,
        unique=True)
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courseAuthor', on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to="thumbnail")
    course_type = models.ManyToManyField(CourseList)
    course_title = models.CharField(max_length=200)
    course_description = models.TextField(verbose_name="Course Overview")
    batch = models.DateTimeField(default=timezone.now, blank=True)
    updatedAt = models.DateTimeField(default=timezone.now, blank=True)
    course_fee = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return f"{self.course_title} by {self.author.first_name} {self.author.last_name} starting from {self.batch}"

    def course_type_detail(self):
        return ",".join([str(x) for x in self.course_type.all()])


class Lesson(models.Model):
    id = models.AutoField(primary_key=True, 
        editable=False,
        unique=True)
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True)
    courses = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    Lesson_Name = models.CharField(max_length=200)
    updatedAt = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.Lesson_Name


class Video(models.Model):
    id = models.AutoField(primary_key=True, 
        editable=False,
        unique=True)
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True)
    Lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    video = models.FileField(upload_to="Video/", blank=True)
    video_description = models.TextField(blank=True)
    notes = models.FileField(upload_to="Notes/", blank=True)
    updatedAt = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    video_name = models.ForeignKey(Video, related_name='video_names', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_asked',
                                on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', on_delete=models.SET_NULL, null=True)
    question_title = models.CharField(max_length=255)
    description = models.TextField()
    question_time = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.question_title


class Answer(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    question_n = models.ManyToManyField(Question, related_name='question_n')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    reply_time = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.answer


class CourseRecorded(Course):
    class Meta:
        proxy = True


class Comment(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey("Profile.myUser", on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField()
    heading = models.CharField(max_length=50)
    comment = models.TextField()
    updatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} gives {self.rating} star"


class Note(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    video = models.ForeignKey(Video, related_name='%(app_label)s_%(class)s_related', on_delete=models.SET_NULL,
                              null=True)
    notes = models.TextField()
    timestamp = models.CharField(max_length=10)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    updatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.by.first_name} at {self.timestamp}"
