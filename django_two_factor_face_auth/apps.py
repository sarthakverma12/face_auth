from django.apps import AppConfig

class DjangoTwoFactorFaceAuthConfig(AppConfig):
    name='django_two_factor_face_auth'

    def ready(self):
        import django_two_factor_face_auth.signals