from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "buyer",
        "farm",
        "product",
        "rating",
        "shortened_text",
        "created_at",
    )

    search_fields = ("reviewer__first_name", "reviewer__last_name", "product__name")

    list_filter = ("rating", "created_at")

    list_display_links = ("buyer",)

    ordering = ("created_at",)

    def shortened_text(self, obj):
        return obj.text[:50] + " ..." if len(obj.text) > 50 else obj.text

    shortened_text.short_description = "Review Text"
