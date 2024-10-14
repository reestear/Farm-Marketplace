import uuid

from django.db import models
from users.models import Buyer


class StatusType(models.TextChoices):
    CART = "Cart", "Cart"
    ORDERED = "Ordered", "Ordered"
    DELIVERED = "Delivered", "Delivered"


class Order(models.Model):
    """
    Order model for storing order information of a buyer.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order Date",
    )

    status = models.CharField(
        max_length=10,
        choices=StatusType.choices,
        verbose_name="Order Status",
        default=StatusType.CART,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Order Amount",
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} by {self.buyer.first_name} {self.buyer.last_name}"
