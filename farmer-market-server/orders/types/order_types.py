from django.db import models


class OrderStatusType(models.TextChoices):
    CART = "Cart", "Cart"
    ORDERED = "Ordered", "Ordered"
    DELIVERED = "Delivered", "Delivered"
