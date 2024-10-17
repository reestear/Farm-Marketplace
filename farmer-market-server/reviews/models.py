import uuid

from core.models.date_stamped_model import DateStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from farms.models.farm_model import Farm
from products.models import Product
from users.models import Buyer, UserType


class Review(DateStampedModel):
    """
    Ternary relation model for storing reviews of a product from farm by a buyer.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"user_type": UserType.BUYER},
        related_name="reviews",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name="Rating",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        error_messages={
            "min_value": "Rating must be between 0 and 5.",
            "max_value": "Rating must be between 0 and 5.",
        },
    )

    text = models.TextField(
        verbose_name="Review Text",
        blank=True,
    )
