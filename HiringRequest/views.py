from django.shortcuts import render
from .models import HiringRequest, EnquiryRequest, Feedback
from .Serializers import HiringRequestSerializer, EnquiryRequestSerializer, FeedbackSerializer
from rest_framework.viewsets import ModelViewSet


class HiringRequestView(ModelViewSet):
    queryset = HiringRequest.objects.all()
    serializer_class = HiringRequestSerializer


class EnquiryRequestView(ModelViewSet):
    queryset = EnquiryRequest.objects.all()
    serializer_class = EnquiryRequestSerializer


class FeedbackView(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
