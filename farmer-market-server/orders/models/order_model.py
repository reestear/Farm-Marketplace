import uuid
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from orders.types.order_types import OrderStatusType
from users.models import Buyer, UserType

from .delivery_model import Delivery
from .order_farm_product_relation import OrderFarmProduct
from .payment_model import Payment


class Order(models.Model):
    """
    Order model for storing order information of a buyer.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": UserType.BUYER},
        related_name="orders",
    )

    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order Date",
    )

    status = models.CharField(
        max_length=10,
        choices=OrderStatusType.choices,
        verbose_name="Order Status",
        default=OrderStatusType.CART,
    )

    # amount = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     verbose_name="Order Amount",
    # )

    @property
    def amount(self):
        """
        Calculate the total amount of the order.
        """
        farm_products: Optional[models.Manager] = getattr(
            self, "order_farm_products", None
        )
        if not farm_products:
            return 0

        return sum(
            order_farm_product.total_price for order_farm_product in farm_products.all()
        )

    def add_product_from_farm(self, farm, product, quantity, price):
        """
        Order should be in cart status to add products.
        For that reason, Order status should by of type "OrderStatusType.CART".
        """
        if self.status != OrderStatusType.CART:
            raise ValueError("Order should be in cart to add products.")

        return OrderFarmProduct.objects.create(
            order=self,
            farm=farm,
            product=product,
            quantity=quantity,
            negotiated_price=price,
        )

    def edit_product_from_farm(self, farm, product, quantity=None, price=None):
        """
        Order should be in cart status to edit products.
        For that reason, Order status should by of type "OrderStatusType.CART".
        """
        if self.status != OrderStatusType.CART:
            raise ValueError("Order should be in cart to edit products.")

        try:
            order_farm_product = OrderFarmProduct.objects.get(
                order=self,
                farm=farm,
                product=product,
            )
            if quantity:
                order_farm_product.quantity = quantity
            if price:
                order_farm_product.negotiated_price = price

            order_farm_product.save()
            return order_farm_product
        except ObjectDoesNotExist:
            raise ValueError("This product does not exist in the cart.")

    def remove_product_from_farm(self, farm, product):
        """
        Order should be in cart status to remove products.
        For that reason, Order status should by of type "OrderStatusType.CART".
        """
        if self.status != OrderStatusType.CART:
            raise ValueError("Order should be in cart to remove products.")

        order_farm_product = OrderFarmProduct.objects.get(
            order=self,
            farm=farm,
            product=product,
        )
        order_farm_product.delete()

    def purchase(self, payment_details, delivery_details):
        """
        Order should be in cart status to purchase.
        For that reason, Order status should by of type "OrderStatusType.CART".
        """
        if self.status != OrderStatusType.CART:
            raise ValueError("Order should be in cart to purchase.")

        self.set_status(OrderStatusType.ORDERED)
        self.save()

        Payment.objects.create(
            order=self,
            method=payment_details["method"],
            amount=payment_details["amount"],
        )

        Delivery.objects.create(
            order=self,
            address=delivery_details["address"],
            delivery_date=delivery_details["delivery_date"],
        )

    def clean(self):
        """
        Check if an active cart already exists for the buyer.

        Raises:
            ValueError
        """
        if (
            self.status == OrderStatusType.CART
            and Order.objects.filter(buyer=self.buyer, status=OrderStatusType.CART)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValueError("An active cart already exists for the buyer.")

        # TODO: Nahhh, some circulation dependency issue here... I'll fix it later
        # if self.status != OrderStatusType.CART:
        #     if not hasattr(self, "payment") or self.payment is None:
        #         raise ValueError(
        #             "A payment must be associated with the order to set the status to ordered."
        #         )

        #     if not hasattr(self, "delivery") or self.payment is None:
        #         raise ValueError(
        #             "A delivery must be associated with the order to set the status to ordered."
        #         )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def set_status(self, status):
        """
        Set the status of the order.

        Raises:
            ValueError: If the status is not a valid choice.
        """
        if status not in [status_type for status_type, _ in OrderStatusType.choices]:
            raise ValueError("Invalid status type.")

        if status == OrderStatusType.CART and self.status in [
            OrderStatusType.ORDERED,
            OrderStatusType.DELIVERED,
        ]:
            raise ValueError(
                "Cannot set the status to cart if the order is already ordered or delivered."
            )

        self.status = status
        self.save()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} by {self.buyer.first_name} {self.buyer.last_name}"
