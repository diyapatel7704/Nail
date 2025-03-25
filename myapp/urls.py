from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('product/<int:id>/',views.product_detail,name='product_details'),
    path('contact',views.contact,name='contact'),
    path('shop-cart/', views.shop_cart, name='shop_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout')
]