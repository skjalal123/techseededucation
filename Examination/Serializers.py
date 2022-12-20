from rest_framework import serializers
from .models import *
from Course.Serializers import *


class Subjects(serializers.ModelSerializer):
    course = CourseListSerial(read_only=True)

    class Meta:
        model = Subject
        fields = "__all__"


class QuestionSerial(serializers.ModelSerializer):
    subjects = Subjects()

    class Meta:
        model = Question
        fields = "__all__"

    def validate(self, attrs):
        print(attrs)
        if attrs["course"] is None and attrs["Subject_Name"] == "":
            raise ValidationError("Course and Subject Name field cannot be null")

        if attrs["course"] is not None and attrs["Subject_Name"] != "":
            raise ValidationError("Only one field is required")


class Options(serializers.ModelSerializer):
    # Question = QuestionSerial(many=False)

    class Meta:
        model = Option
        fields = '__all__'

