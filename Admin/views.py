from django.shortcuts import render
from .Serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class TermOfUseView(ModelViewSet):
    queryset = TermOfUser.objects.all()
    serializer_class = TermOfUseSerializer
    http_method_names = ['get']


class FrequentlyAskedQuestionView(ModelViewSet):
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = FrequentlyAskedQuestionSerializer
    http_method_names = ['get']


class FoundersView(ModelViewSet):
    queryset = Founder.objects.all()
    serializer_class = FoundersSerializer
    http_method_names = ['get']
