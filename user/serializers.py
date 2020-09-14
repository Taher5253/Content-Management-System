from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class Cms_userSerializer(serializers.ModelSerializer):

    class Meta():
        model = Cms_user
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta():
        model = Categories
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    #content_author = Cms_userSerializer(read_only=True, )
    class Meta():
        model = Content
        fields = '__all__'


class ContentReadSerializer(ContentSerializer):
    content_author = Cms_userSerializer(read_only=True,)
    class Meta():
        model = Content
        fields = '__all__'

class content_categorySerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True,)
    category = CategoriesSerializer(read_only=True,)
    class Meta():
        model = content_category
        fields = '__all__'