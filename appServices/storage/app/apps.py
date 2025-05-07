from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        from .grpc.grpcServers.storageGrpc import serve
        import threading
        threading.Thread(target=serve).start()
