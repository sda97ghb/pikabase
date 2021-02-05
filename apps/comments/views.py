from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.comments import models


class CommentsTaskSerializer(ModelSerializer):
    class Meta:
        model = models.CommentsTask
        fields = "__all__"


class CommentsTaskPostSerializer(ModelSerializer):
    class Meta:
        model = models.CommentsTask
        fields = ["url"]


class CommentsTaskViewSet(ModelViewSet):
    queryset = models.CommentsTask.objects.all()
    serializer_class = CommentsTaskSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentsTaskPostSerializer
        return self.serializer_class
