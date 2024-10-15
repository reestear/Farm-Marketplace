# from django.db.models import signals
# from django.dispatch import receiver

# from .models import Delivery, Order, Payment, StatusType


# @receiver(signals.pre_save, sender=Order)
# def create_payment_delivery(sender, instance, **kwargs):
#     if instance.status in [StatusType.ORDERED, StatusType.DELIVERED]:
#         # Create Payment if it doesn't exist
#         if not hasattr(instance, "payment"):
#             Payment.objects.get_or_create(order=instance)
#         # Create Delivery if it doesn't exist
#         if not hasattr(instance, "delivery"):
#             Delivery.objects.get_or_create(order=instance)
