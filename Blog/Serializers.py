from rest_framework import serializers
from .models import Blog, BlogType


class BlogTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = BlogType
        fields = '__all__'


class BlogsSerializers(serializers.ModelSerializer):
    blog_type = BlogTypeSerializers()

    class Meta:
        model = Blog
        fields = '__all__'