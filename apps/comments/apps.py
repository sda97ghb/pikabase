from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = "apps.comments"

    def ready(self):
        # Connect signals
        import apps.comments.signals
        type(apps.comments.signals)
