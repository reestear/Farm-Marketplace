from django.contrib import admin

from .models import Delivery, Order, Payment
from .models.order_farm_product_relation import OrderFarmProduct


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0

    readonly_fields = [field.name for field in Payment._meta.get_fields()]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 0

    readonly_fields = [field.name for field in Delivery._meta.get_fields()]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class OrderFarmProductInline(admin.StackedInline):
    model = OrderFarmProduct
    extra = 0

    readonly_fields = [field.name for field in OrderFarmProduct._meta.get_fields()]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "order_date", "status")

    search_fields = ("id", "buyer__first_name", "buyer__last_name")

    list_filter = ("status", "buyer__first_name", "buyer__last_name")

    list_display_links = ("id", "buyer")

    inlines = [PaymentInline, DeliveryInline, OrderFarmProductInline]

    ordering = ("id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "payment_date")

    list_filter = ("payment_date",)

    search_fields = ("order__id", "method")

    list_display_links = ("order",)

    ordering = ("-payment_date",)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("order", "delivery_date", "status")

    list_filter = ("delivery_date", "status")

    search_fields = ("order__id",)

    list_display_links = ("order",)

    ordering = ("-delivery_date",)
