import uuid

from django.db import models
from products.models import Product
from users.models import Farmer


class Farm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
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
        return f"{self.name}"
