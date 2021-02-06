import logging

from dramatiq import actor

from apps.comments.models import CommentsTask, StatusChoices

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

    comments_task.status = StatusChoices.ERROR.value
    comments_task.status_message = "Processing task is not implemented"
    comments_task.save()
