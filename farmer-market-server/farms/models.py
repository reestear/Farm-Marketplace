import uuid

from django.core.exceptions import ValidationError
from django.db import models
from products.models import Product, UnitType
from users.models import Farmer, UserType


class Farm(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name="farms",
    )

    products = models.ManyToManyField(
        Product,
        through="FarmProduct",
        related_name="farms",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Farm Name",
    )

    size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Farm Size (in hectares)",
    )

    location = models.CharField(
        max_length=255,
        verbose_name="Farm Location",
    )

    resources = models.TextField(
        verbose_name="Available Resources",
        blank=True,
    )

    class Meta:
        verbose_name = "Farm"
        verbose_name_plural = "Farms"

    def __str__(self):
        return (
            f"{self.name} (owned by {self.farmer.first_name} {self.farmer.last_name})"
        )


class FarmProduct(models.Model):
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Quantity",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Product Description",
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Image URL",
    )

    def clean(self):
        super().clean()
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

    def __str__(self):
        return f"Product: {self.product.name} from Farm: {self.farm.name}"
