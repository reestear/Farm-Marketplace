from django.contrib import admin
from farms.models import FarmProduct

from .models import Product


class FarmProductInline(admin.StackedInline):
    model = FarmProduct
    extra = 0
    # readonly_fields = ["farm", "price", "quantity"]
    readonly_fields = [field.name for field in FarmProduct._meta.get_fields()]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding FarmProduct from Product admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "description")

    search_fields = ("name", "category")

    list_display_links = ("id", "name")

    inlines = [FarmProductInline]

    ordering = ("id",)
