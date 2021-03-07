from rest_framework.decorators import action
from rest_framework.fields import ReadOnlyField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound

from apps.comments import models
from apps.posts.models import Post


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

    @action(detail=False, url_path="of-post/(?P<post_pk>[0-9]+)")
    def of_post(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")

        queryset = post.comments.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="of-post/(?P<post_pk>[0-9]+)/top")
    def top_comments_of_post(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found.")

        queryset = post.comments.filter(parent_comment=None)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path="top-branch")
    def top_branch(self, request, pk):
        comment = models.Comment.objects.get(pk=pk)

        branch = []
        while True:
            comment = comment.children_comments.order_by("-rating").first()
            if comment is None:
                break
            branch.append(comment)

        serializer = self.get_serializer(branch, many=True)
        return Response(serializer.data)
