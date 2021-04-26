from django.apps import AppConfig

class UserConfig(AppConfig):
    name='users'

    def ready(self):
        import django_two_factor_face_auth.signals