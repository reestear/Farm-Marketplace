from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from farms.models.farm_model import Farm
from products.models import Product, UnitType


class OrderFarmProduct(models.Model):
    """
    Ternary relation model for storing the products of a farm in an order.
    """

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="order_farm_products",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="order_farm_products",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="order_farm_products",
    )

    negotiated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Negotiated Price",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Quantity",
    )

    @property
    def total_price(self) -> Decimal:
        """
        Calculate the total price of the product.
        """
        return self.negotiated_price * self.quantity

    def clean(self):
        super().clean()

        # If for some reason the product is not specified when the entry is already created, return None
        if not self.product:
            return None

        # Check if the farm and product are specified during creation
        if not self.pk:
            if not self.farm:
                raise ValidationError("Farm must be specified during creation.")
            if not self.product:
                raise ValidationError("Product must be specified during creation.")

            # Check if the farm and product has the entry in FarmProduct
            if not self.farm.products.filter(id=self.product.id).exists():
                raise ValidationError(
                    "Farm and Product must have a relation in FarmProduct."
                )

        if self.product.unit_type in [
            UnitType.KILOGRAMS,
            UnitType.GRAMS,
            UnitType.LITERS,
        ]:
            if self.quantity < 0:
                raise ValidationError(
                    "Quantity must be a positive value for measured products."
                )
        elif self.product.unit_type == UnitType.PIECES and not self.quantity % 1 != 0:
            raise ValidationError(
                "Quantity must be an integer for products sold in pieces."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Order Farm Product"
        verbose_name_plural = "Order Farm Products"
        unique_together = ("order", "farm", "product")

    def __str__(self):
        return f"Order: {self.order.id}, Farm: {self.farm.name if self.farm else None}, Product: {self.product.name if self.product else None}"
