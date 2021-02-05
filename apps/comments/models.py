from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    PROCESSING = "processing", _("Processing")
    COMPLETED = "completed", _("Completed")
    ERROR = "error", _("Error")


class CommentsTask(models.Model):
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("Post URL"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        help_text=_("Date and time when the task was created"),
    )
    fetched_at = models.DateTimeField(
        verbose_name=_("Fetched at"),
        help_text=_("Date and time when the post page was fetched"),
        blank=True,
        null=True,
    )
    finished_at = models.DateTimeField(
        verbose_name=_("Finished at"),
        help_text=_("Date and time when the task was finished"),
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=100,
        verbose_name=_("Status"),
        help_text=_("Current status"),
        choices=StatusChoices.choices,
    )


@receiver(pre_save, sender=CommentsTask)
def set_comments_task_created_at(sender, **kwargs):
    instance = kwargs.get("instance")
    if not instance.created_at:
        instance.created_at = timezone.now()
    if not instance.status:
        instance.status = StatusChoices.PENDING.value
