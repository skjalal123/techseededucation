from Profile.Serializers import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import *

from .models import *


class CourseListSerial(serializers.ModelSerializer):
    class Meta:
        model = CourseList
        fields = '__all__'


class CourseSerial(serializers.ModelSerializer):
    course_type = serializers.ReadOnlyField(source='CourseList.CourseList')

    class Meta:
        model = Course
        #fields = '__all__'
        exclude = ('id',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = User(instance.author).data
        return rep

    def create(self, validated_data):
        users = self.context['request'].user
        if user.is_student:
            return Response({"Invalid": "Invalid user"}, status=HTTP_405_METHOD_NOT_ALLOWED)
        if validated_data['is_live_Lectures']:
            validated_data['is_free_course'] = False
        else:
            validated_data['is_free_course'] = True
        course = Course.objects.create(
            course_title=validated_data['course_title'],
            course_type=validated_data['course_type'],
            course_description=validated_data['course_description'],
            Level=validated_data['Level']
        )
        course.save()
        return Response(data=Course, status=HTTP_201_CREATED)


class LessonSerial(serializers.ModelSerializer):
    courses = CourseSerial()

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(LessonSerial, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Lesson
        fields = '__all__'


class VideoSerial(serializers.ModelSerializer):
    Lessons = LessonSerial()

    class Meta:
        model = Video
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(VideoSerial, self).__init__(many=many, *args, **kwargs)


class QuestionSerial(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user:
            questions = Question.objects.create(
                description=validated_data['description'],
                question_title=validated_data['question_title'],
                student=user,
                video_name=validated_data['video_name'],
                author=validated_data['video_name'].Lessons.courses.author
            )
            questions.save()

            return questions


class Answer_Serial(serializers.ModelSerializer):
    video = VideoSerial()

    class Meta:
        model = Answer
        fields = '__all__'


class NoteSerial(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if user:
            notes = Note.objects.create(
                by=user,
                notes=validated_data['notes'],
                timestamp=validated_data['timestamp'],
                video=validated_data['video']
            )
            notes.save()

            return notes

        return Response({'Authorization': "Please Login First"}, status=HTTP_401_UNAUTHORIZED)
