from django.db import models
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
    status_message = models.TextField(
        verbose_name=_("Status message"),
        help_text=_("Status message such as error description"),
    )

    @property
    def is_finished(self):
        return self.status == StatusChoices.COMPLETED.value or StatusChoices.ERROR.value

    def __str__(self):
        return f"CommentsTask #{self.pk}: {self.status} {self.url} " \
               f"{self.created_at} {self.fetched_at} {self.finished_at}: " \
               f"{self.status_message}"

    def __repr__(self):
        return f"CommentsTask #{self.pk}: {self.status} {self.url} " \
               f"{self.created_at} {self.fetched_at} {self.finished_at}: " \
               f"{self.status_message}"
