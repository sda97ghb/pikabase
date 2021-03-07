from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("comments/", include("apps.comments.urls")),
    path("pikabu-users/", include("apps.pikabu_users.urls")),
    path("posts/", include("apps.posts.urls")),
    path("admin/", admin.site.urls),
]
