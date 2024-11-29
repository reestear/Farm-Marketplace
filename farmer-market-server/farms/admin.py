from django.contrib import admin

from .models import Farm, FarmProduct, FarmProductImage


class FarmProductImageInline(admin.StackedInline):
    model = FarmProductImage
    extra = 1
    readonly_fields = ["uploaded_at"]


@admin.register(FarmProduct)
class FarmProductAdmin(admin.ModelAdmin):
    list_display = ("id", "farm", "product", "price", "quantity")
    search_fields = ("farm__name", "product__name")
    list_display_links = ("id", "farm", "product")
    ordering = ("id",)
    inlines = [FarmProductImageInline]


class FarmProductInline(admin.StackedInline):
    model = FarmProduct
    extra = 1
    autocomplete_fields = ["product"]

    show_change_link = True


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
