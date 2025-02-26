# Generated by Django 5.0 on 2024-11-30 12:10

import django.core.validators
import products.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Product Name")),
                ("category", models.CharField(max_length=100, verbose_name="Category")),
                (
                    "unit_type",
                    models.CharField(
                        choices=[
                            ("kg", "Kilograms"),
                            ("g", "Grams"),
                            ("l", "Liters"),
                            ("pcs", "Pieces"),
                        ],
                        max_length=10,
                        verbose_name="Unit Type",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Product Description"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.product_image_upload_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png"]
                            )
                        ],
                        verbose_name="Product Image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
    ]
