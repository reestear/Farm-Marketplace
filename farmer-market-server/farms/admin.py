from django.contrib import admin

from .models import Farm, FarmProduct


class FarmProductInline(admin.StackedInline):
    model = FarmProduct
    extra = 1  # Number of extra forms to display
    autocomplete_fields = ["product"]


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "farmer", "size", "location")

    search_fields = ("name", "location", "farmer__first_name", "farmer__last_name")

    inlines = [FarmProductInline]

    list_display_links = (
        "id",
        "name",
    )

    ordering = ("id",)
