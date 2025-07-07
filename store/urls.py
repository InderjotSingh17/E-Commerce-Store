from django.urls import path
from .views import CreateCheckoutSession
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('decrease-quantity/<int:pk>/', decrease_quantity, name='decrease-quantity'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-summary/<int:pk>/', OrderSummaryView.as_view(), name='order-summary'),
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
