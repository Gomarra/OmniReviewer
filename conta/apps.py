from django.apps import AppConfig


class ContaConfig(AppConfig):
    name = 'conta'

    def ready(self):
        import conta.signals
