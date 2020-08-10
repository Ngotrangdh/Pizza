from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addtocart", views.add_to_cart, name="add_to_cart"),
    path("updateitemquantity", views.update_item_quantity, name="update_item_quantity"),
    path("deletecart", views.delete_cart, name="delete_cart"),
    path("cart", views.get_cart, name="cart"),
    path("placeorder", views.place_order, name="place_order"),
    path("ordersummary/<int:order_id>", views.order_summary, name="order_summary"),
    path("orderhistory", views.order_history, name="order_history"),
]
