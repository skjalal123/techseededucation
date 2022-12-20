from rest_framework import serializers
from .models import *


class TermOfUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermOfUser
        fields = '__all__'


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestion
        fields = '__all__'


class FoundersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = '__all__'