from django.db import models
from orders.types.order_types import OrderStatusType


class DeliveryStatus(models.TextChoices):
    DELIVERING = "Delivering", "Delivering"
    DELIVERED = "Delivered", "Delivered"


class Delivery(models.Model):
    """
    Weak Entity: Delivery model for storing delivery information of an order.
    """

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        related_name="delivery",
        limit_choices_to={
            "status__in": [OrderStatusType.ORDERED, OrderStatusType.DELIVERED],
        },
    )

    delivery_date = models.DateTimeField(
        auto_now_add=False,
        verbose_name="Delivery Date",
    )

    status = models.CharField(
        max_length=10,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.DELIVERING,
        verbose_name="Delivery Status",
    )

    address = models.CharField(
        max_length=200,
        verbose_name="Delivery Address",
    )

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return f"Delivery for Order: {self.order.id if self.order else None}"
