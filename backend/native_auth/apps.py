from django.apps import AppConfig


class NativeAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'native_auth'

    def ready(self) -> None:
        import native_auth.signals