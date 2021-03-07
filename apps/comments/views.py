from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.comments import models


class CommentsTaskSerializer(ModelSerializer):
    created_at = ReadOnlyField()
    fetched_at = ReadOnlyField()
    finished_at = ReadOnlyField()
    status = ReadOnlyField()
    status_message = ReadOnlyField()

    class Meta:
        model = models.CommentsTask
        fields = "__all__"


class CommentsTaskViewSet(ModelViewSet):
    queryset = models.CommentsTask.objects.all()
    serializer_class = CommentsTaskSerializer


class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
