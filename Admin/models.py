from django.db import models


# Create your models here.
class TermOfUser(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class FrequentlyAskedQuestion(models.Model):
    questions = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.questions


class Founder(models.Model):
    profileImage = models.FileField(upload_to='profile')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    contact = models.EmailField()

    def __str__(self):
        return self.name
