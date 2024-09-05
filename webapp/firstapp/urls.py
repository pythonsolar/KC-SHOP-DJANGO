from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('tracking', TrackingPage, name='tracking'),
    path('contact', Contact, name='contact'),
    path('ask', Ask, name='ask' ),
    path('questions',Questions, name='questions'),
    path('answer/<int:askid>',Answer, name='answer'),
    path('blogs',Posts, name='posts'),
    path('blogs/<slug:slug>/',PostDetail, name='post-detail'),
    path('register',Register,name='register'),
    path('login',Login,name='login'),
    path('products',AllProduct, name="all-product"),
    path('discount',DiscountPage, name="discount"),
    path('product/<slug:slug>/',ProductDetail, name='product-detail'),
    path('tracking/<str:tid>/', TrackingOrderId, name='tracking-order-id-page'),
    path('add-cart/<int:pid>', AddToCart, name='add-to-cart'),
    path('cart/',MyCart, name='my-cart'),
    path('editcart/',MyCartEdit, name='my-cart-edit'),
    path('checkout/',Checkout, name='checkout'),
    path('orders/', CartOrderProduct, name="cart-order-product"),
    path('upload-slip/<str:order_id>/', UploadSlipOrder, name="upload-slip-order"),
    path('customer-all-order/', CustomerAllOrder, name="customer-all-order"),
    path('update-status/<str:order_id>/<str:status>/', UpdatePaid, name="update-status"),
    path('update-tracking/<str:order_id>/', CartOrderUpdateTracking, name='cart-order-update-tracking'),
    path('my-order/<str:order_id>/', MyOrder, name='my-order'),
]
