from django.apps import AppConfig


class ContadorDeCaloriasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contador_de_calorias"

    def ready(self):
        import contador_de_calorias.signals