from django.db import models


class DateStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Date",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Update Date",
    )

    class Meta:
        abstract = True
