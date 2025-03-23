from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('product_details',views.product_details,name='product_details'),
    path('shop-cart/',views.shop_cart,name='shop_cart'),
    path('contact',views.contact,name='contact'),
    path('checkout',views.checkout,name='checkout'),
    path('login/',views.login,name='login'),
    path('signup',views.signup,name='signup')
]