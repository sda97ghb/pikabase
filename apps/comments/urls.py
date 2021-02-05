from rest_framework.routers import DefaultRouter

from apps.comments.views import CommentsTaskViewSet

router = DefaultRouter()
router.register("tasks", CommentsTaskViewSet, basename="comments_tasks")
urlpatterns = router.urls
