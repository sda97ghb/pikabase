from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("The url of the post on pikabu.ru")
    )

    def __str__(self):
        return f"Post #{self.pk}: {self.url}"

    def __repr__(self):
        return f"Post #{self.pk}: {self.url}"
