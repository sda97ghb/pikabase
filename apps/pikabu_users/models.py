from django.db import models
from django.utils.translation import gettext_lazy as _


class PikabuUser(models.Model):
    username = models.CharField(
        max_length=20,
        verbose_name=_("Username"),
        help_text=_("The username of the user, e.g. Destroyeer"),
    )

    def __str__(self):
        return f"PikabuUser #{self.pk}: {self.username}"

    def __repr__(self):
        return f"PikabuUser #{self.pk}: {self.username}"
