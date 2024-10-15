from django.db import models
from orders.types.order_types import OrderStatusType


class PaymentMethod(models.TextChoices):
    KASPI = "Kaspi", "Kaspi"
    JUSAN = "Jusan", "Jusan"
    TBANK = "TBank", "TBank"


class Payment(models.Model):
    """
    Weak Entity: Payment model for storing payment information of an order.
    """

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        related_name="payment",
        limit_choices_to={
            "status__in": [OrderStatusType.ORDERED, OrderStatusType.DELIVERED],
        },
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Payment Date",
    )

    method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        verbose_name="Payment Method",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Payment Amount",
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment for Order: {self.order.id if self.order else None}"
