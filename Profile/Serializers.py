from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.core.mail import EmailMessage


class User(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=myUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = myUser
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = myUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            is_student=validated_data['is_student'],
            is_teacher=validated_data['is_teacher'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()
        otp = OneTimePassword(profileId=user).save()
        html_content = f"<p>This is your OTP <h1>{otp}<h1></p>"
        msg = EmailMessage("Activate your Account", html_content,"skjalal149@gmail.com",[validated_data['email']])
        return user


class Qualification(serializers.ModelSerializer):
    class Meta:
        model = qualification
        exclude = ['uid']


class Achievement(serializers.ModelSerializer):
    class Meta:
        model = achievement
        exclude = ['uid']


class Experiance(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ['uid']


class myProfile(serializers.Serializer):
    user = User()
    qualification = Qualification()
    achievement = Achievement()
    experiance = Experiance()