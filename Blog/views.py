from django.shortcuts import render
from .models import Blog
from .Serializers import BlogsSerializers
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class BlogsView(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogsSerializers
    lookup_field = 'slug'