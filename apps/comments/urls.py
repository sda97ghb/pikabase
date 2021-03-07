from rest_framework.routers import DefaultRouter

from apps.comments.views import CommentsTaskViewSet, CommentViewSet

app_name = "comments"

router = DefaultRouter()
router.register("tasks", CommentsTaskViewSet, basename="comments_tasks")
router.register("comments", CommentViewSet, basename="comments")
urlpatterns = router.urls
