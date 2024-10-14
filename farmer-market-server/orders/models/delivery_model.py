from django.db import models

from .order_model import Order


class DeliveryStatus(models.TextChoices):
    DELIVERING = "Delivering", "Delivering"
    DELIVERED = "Delivered", "Delivered"


class Delivery(models.Model):
    """
    Weak Entity: Delivery model for storing delivery information of an order.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        related_name="deliveries",
    )

    delivery_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Delivery Date",
    )

    status = models.CharField(
        max_length=10,
        choices=DeliveryStatus.choices,
        verbose_name="Delivery Status",
    )

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return f"Delivery for Order: {self.order.id if self.order else None}"
