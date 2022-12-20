from django.db import models
import uuid
from django.core.exceptions import ValidationError


# Create your models here.


class Subject(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    course = models.ForeignKey('Course.CourseList', on_delete=models.CASCADE, related_name="Courses", blank=True, null=True)
    thumbnail = models.FileField(upload_to="exam-thumbnail")
    Subject_Name = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.Subject_Name} from {self.course.CourseList} "

    def clean(self):
        if not self.course and not self.Subject_Name:  # This will check for None or Empty
            raise ValidationError('Course or Subject Name:- Even one of course or Subject_Name should have a value.')


class Question(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    subjects = models.ForeignKey(to=Subject, related_name="subject", on_delete=models.SET_NULL, null=True)
    questions = models.TextField(blank=True, help_text="Enter the Question")
    images = models.FileField(upload_to="Quiz_Questions", blank=True)

    def __str__(self):
        return f"{self.questions} from {self.subjects.Subject_Name}"


class Option(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    Question = models.ForeignKey(to=Question, related_name="Options", on_delete=models.CASCADE)
    option = models.TextField(help_text="Enter the options", blank=True)
    imagesOptions = models.FileField(upload_to="QuizImages", blank=True, help_text="Enter the Image options If required", )
    is_correct_answer = models.BooleanField(default=False,
                                            help_text="Check if this image or option is correct answer for this "
                                                      "question")

