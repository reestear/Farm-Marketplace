import uuid

from django.db import models


class UnitType(models.TextChoices):
    KILOGRAMS = "kg", "Kilograms"
    GRAMS = "g", "Grams"
    LITERS = "l", "Liters"
    PIECES = "pcs", "Pieces"


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Product Name",
    )

    category = models.CharField(
        max_length=100,
        verbose_name="Category",
    )

    unit_type = models.CharField(
        max_length=10,
        choices=UnitType.choices,
        verbose_name="Unit Type",
        null=False,
        blank=False,
    )

    description = models.TextField(
        verbose_name="Product Description",
        blank=True,
    )

    image = models.ImageField(
        upload_to="products/",
        verbose_name="Product Image",
        blank=True,
        null=True,
        # validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])]
        # default="products/default.jpg"
    )

    # def product_image_upload_to(self, filename):
    #     # Store files under products/<product_id>/<filename>
    #     return f"products/{self.id}/{filename}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
