from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.posts import models


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = "__all__"


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
