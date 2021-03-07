import logging

from dramatiq import actor

from apps.comments.models import CommentsTask, StatusChoices, Comment
from apps.pikabu_users.models import PikabuUser
from apps.posts.models import Post
from pikabu.api.comments import story_comments

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@actor(queue_name="pikabase_comments")
def process_comments(comments_task_pk):
    try:
        comments_task = CommentsTask.objects.get(pk=comments_task_pk)
    except CommentsTask.DoesNotExist:
        log.warning("CommentsTask does not exist: pk=%r", comments_task_pk)
        return

    log.info("Processing %r", comments_task)

    comments_task.status = StatusChoices.PROCESSING.value
    comments_task.status_message = "Fetching comments"
    comments_task.save()

    post, created = Post.objects.get_or_create(url=comments_task.url)
    if created:
        log.info("Created post %s", post.url)

    affected_comments = []
    for comment in story_comments(story_url=comments_task.url):
        pikabu_user, created = PikabuUser.objects.get_or_create(
            username=comment.username
        )
        if created:
            log.info("Created user %s", pikabu_user.username)

        comment, created = Comment.objects.update_or_create(
            pikabu_id=comment.id,
            defaults={
                "pikabu_parent_id":comment.parent_id,
                "user":pikabu_user,
                "text":comment.text,
                "date":comment.date,
                "rating":comment.rating,
                "post":post,
            }
        )
        affected_comments.append(comment)

    comments_task.status_message = "Setting up parent comments"
    comments_task.save()

    for comment in affected_comments:
        if comment.pikabu_parent_id is not None and comment.parent_comment is None:
            comment.parent_comment = Comment.objects.get(
                pikabu_id=comment.pikabu_parent_id
            )
            comment.save()

    comments_task.status = StatusChoices.COMPLETED.value
    comments_task.status_message = "Success"
    comments_task.save()
