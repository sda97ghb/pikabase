from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.comments.models import CommentsTask, StatusChoices
from apps.comments.tasks import process_comments


@receiver(pre_save, sender=CommentsTask)
def set_comments_task_default_attributes(sender, **kwargs):
    instance = kwargs.get("instance")
    if not instance.created_at:
        instance.created_at = timezone.now()
    if not instance.status:
        instance.status = StatusChoices.PENDING.value


@receiver(post_save, sender=CommentsTask)
def run_pending_comments_task(sender, **kwargs):
    instance = kwargs.get("instance")
    if instance.status == StatusChoices.PENDING.value:
        process_comments.send(instance.pk)
