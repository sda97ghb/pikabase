from rest_framework.routers import DefaultRouter

from apps.pikabu_users.views import PikabuUserViewSet

app_name = "pikabu_users"

router = DefaultRouter()
router.register("users", PikabuUserViewSet, basename="users")
urlpatterns = router.urls
