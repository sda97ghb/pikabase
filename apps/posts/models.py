from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("The url of the post on pikabu.ru."),
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_("Is processed?"),
        help_text=_("Does the post contain processed values or url only?"),
    )
    user = models.ForeignKey(
        "pikabu_users.PikabuUser",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name=_("User"),
        help_text=_("The creator of the post."),
    )

    def __str__(self):
        return f"Post #{self.pk}: {self.url}"

    def __repr__(self):
        return f"Post #{self.pk}: {self.url}"
