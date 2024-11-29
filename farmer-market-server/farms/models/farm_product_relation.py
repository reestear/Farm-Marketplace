from django.core.exceptions import ValidationError
from django.db import models
from products.models import Product, UnitType

from .farm_model import Farm


def farm_product_image_upload_to(inst, filename):
    return f"farm-products/{inst.farm_product.id}/{filename}"


class FarmProductImage(models.Model):
    farm_product = models.ForeignKey(
        "FarmProduct",
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to=farm_product_image_upload_to,
        verbose_name="Farm Product Image",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()

        self.image = None
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Image for Farm Product: {self.farm_product.product.name} from Farm: {self.farm_product.farm.name}"


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

    class Meta:
        unique_together = ("farm", "product")

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
