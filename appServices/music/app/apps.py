from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        import threading
        from app.grpc.grpcServers.musicGrpc import serve
        threading.Thread(target=serve, daemon=True).start()