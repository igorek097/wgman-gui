from django.apps import AppConfig


class WireguardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wireguard'
    
    def ready(self) -> None:
        import wireguard.signals
