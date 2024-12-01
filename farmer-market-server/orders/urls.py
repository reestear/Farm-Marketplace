from django.urls import path

from .views import (
    AddProductToOrderView,
    BuyerEditProductInOrderView,
    BuyerOrderListView,
    CartFarmProductListView,
    CreateOrderView,
    FarmerEditProductInOrderView,
    OrderFarmProductListView,
    PurchaseOrderView,
    RemoveProductFromOrderView,
)

urlpatterns = [
    path("orders/create-cart/", CreateOrderView.as_view(), name="create-cart-order"),
    path("orders/", BuyerOrderListView.as_view(), name="buyer_orders"),
    path(
        "orders/add-product/",
        AddProductToOrderView.as_view(),
        name="add_product_to_order",
    ),
    path(
        "orders/buyer-edit-product/<uuid:farm_id>/<uuid:product_id>/",
        BuyerEditProductInOrderView.as_view(),
        name="buyer_edit_product_in_order",
    ),
    path(
        "orders/<uuid:order_id>/farmer-edit-product/<uuid:farm_id>/<uuid:product_id>/",
        FarmerEditProductInOrderView.as_view(),
        name="farmer_edit_product_in_order",
    ),
    path(
        "orders/remove-product/<uuid:farm_id>/<uuid:product_id>/",
        RemoveProductFromOrderView.as_view(),
        name="remove_product_from_order",
    ),
    path(
        "orders/purchase/",
        PurchaseOrderView.as_view(),
        name="purchase_order",
    ),
    path(
        "order-farm-products/",
        OrderFarmProductListView.as_view(),
        name="order-farm-product-list",
    ),
    path(
        "cart-farm-products/",
        CartFarmProductListView.as_view(),
        name="cart-farm-product-list",
    ),
]
