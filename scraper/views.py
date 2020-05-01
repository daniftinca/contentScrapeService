from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from scraper import serializers
from scraper.model.content import Content
from scraper.serializers import ContentSerializer, UserSerializer


contents = {
        1: Content(title='Demo', text_content='xordoquy'),
        2: Content(title='Demo', text_content='xordoquy'),
        3: Content(title='Demo', text_content='xordoquy'),
    }

def get_next_content_id():
    return max(contents) + 1

class ContentViewSet(viewsets.ViewSet):
    """
    API endpoint to get all content.
    """
    serializer_class = ContentSerializer



    def get_serializer(self):
        return self.serializer_class()

    def list(self, request):
        serializer = serializers.ContentSerializer(
            instance=contents.values(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.ContentSerializer(data=request.data)
        if serializer.is_valid():

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            content = contents[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ContentSerializer(instance=content)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            content = contents[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ContentSerializer(
            data=request.data, instance=content)
        if serializer.is_valid():
            content = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            content = contents[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ContentSerializer(
            data=request.data,
            instance=content,
            partial=True)
        if serializer.is_valid():
            content = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            content = contents[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
