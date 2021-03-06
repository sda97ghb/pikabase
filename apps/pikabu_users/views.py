from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.pikabu_users import models


class PikabuUserSerializer(ModelSerializer):
    class Meta:
        model = models.PikabuUser
        fields = "__all__"


class PikabuUserViewSet(ModelViewSet):
    queryset = models.PikabuUser.objects.all()
    serializer_class = PikabuUserSerializer
