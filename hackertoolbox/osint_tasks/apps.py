from django.apps import AppConfig


class OsintTasksConfig(AppConfig):
    name = "osint_tasks"

    def ready(self):
        import osint_tasks.signals  # signals integration as soon as the app is ready
