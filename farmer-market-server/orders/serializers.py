from farms.models import Farm
from orders.models import Delivery, Order, OrderFarmProduct, Payment
from products.models import Product
from rest_framework import serializers


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "buyer", "status", "order_date")
        read_only_fields = ("id", "buyer", "status", "order_date")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "method", "amount")
        read_only_fields = ("id", "method", "amount")


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ("id", "address", "delivery_date")
        read_only_fields = ("id", "address", "delivery_date")


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_date",
            "status",
            "amount",
            "payment",
            "delivery",
        ]


class OrderFarmProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFarmProduct
        fields = [
            "id",
            "order",
            "farm",
            "product",
            "negotiated_price",
            "quantity",
            "total_price",
        ]


class AddProductSerializer(serializers.Serializer):
    farm_id = serializers.UUIDField(required=True)
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    def validate(self, attrs):
        # Validate that the farm and product exist
        farm = Farm.objects.filter(id=attrs["farm_id"]).first()
        if not farm:
            raise serializers.ValidationError("Farm not found.")

        product = Product.objects.filter(id=attrs["product_id"]).first()
        if not product:
            raise serializers.ValidationError("Product not found.")

        attrs["farm"] = farm
        attrs["product"] = product
        return attrs


class EditProductSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        if not attrs.get("quantity") and not attrs.get("price"):
            raise serializers.ValidationError(
                "At least one field (quantity or price) must be provided."
            )
        return attrs


class BuyerEditProductSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        if not attrs.get("quantity"):
            raise serializers.ValidationError("The field quantity must be provided.")
        return attrs


class FarmerEditProductSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        if not attrs.get("price"):
            raise serializers.ValidationError("The price quantity must be provided.")
        return attrs


class RemoveProductSerializer(serializers.Serializer):
    farm_id = serializers.UUIDField(required=True)
    product_id = serializers.UUIDField(required=True)


class PurchaseOrderSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(
        choices=["Kaspi", "Jusan", "TBank"], required=True
    )
    payment_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True
    )
    delivery_address = serializers.CharField(max_length=200, required=True)
    delivery_date = serializers.DateTimeField(required=True)
