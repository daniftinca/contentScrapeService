from django.contrib.auth.models import User, Group
from rest_framework import serializers

from scraper.model.content import Content


class ContentSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=256)
    text_content = serializers.CharField()

    def create(self, validated_data):
        return Content(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']