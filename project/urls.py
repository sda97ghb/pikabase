from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("comments/", include("apps.comments.urls")),
    path("admin/", admin.site.urls),
]
