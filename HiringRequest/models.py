from django.db import models


# Create your models here.
class HiringRequest(models.Model):
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=150)
    official_email = models.EmailField()
    phone = models.PositiveBigIntegerField()

    def __str__(self):
        return f" {self.full_name} {self.designation} from {self.company} want to hire for {self.position}"


class EnquiryRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.full_name}"


class Feedback(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.full_name}"