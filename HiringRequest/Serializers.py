from rest_framework import serializers
from .models import HiringRequest, EnquiryRequest, Feedback


class HiringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringRequest
        fields = '__all__'


class EnquiryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryRequest
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'