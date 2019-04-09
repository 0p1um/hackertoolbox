from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = "search"

    def ready(self):
        import search.signals  # signals integration as soon as the app is ready
