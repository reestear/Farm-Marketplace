from django.contrib import admin

from .models import Delivery, Order, Payment


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 1


class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "order_date", "amount", "status")

    search_fields = ("id", "buyer__first_name", "buyer__last_name")

    list_filter = ("status", "buyer__first_name", "buyer__last_name")

    list_display_links = ("id", "buyer")

    inlines = [PaymentInline, DeliveryInline]

    ordering = ("id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "amount", "payment_date")

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
