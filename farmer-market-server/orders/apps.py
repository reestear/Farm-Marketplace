# import importlib

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    # def ready(self):
    #     super().ready()
    #     importlib.import_module("orders.signals")
