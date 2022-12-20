from rest_framework import serializers
from .models import Cart
from Profile.Serializers import User
from Course.Serializers import CourseSerial


class CartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=250);
    student = User()
    course = CourseSerial()

    class Meta:
        model = Cart
        fields = '__all__'
