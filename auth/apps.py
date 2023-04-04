from django.apps import AppConfig
from rest_framework_api_key.models import APIKey

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'

    def ready(self):
        api_key, key = APIKey.objects.create_key(name="my-remote-service")
        print(f"API key: {api_key.key}")