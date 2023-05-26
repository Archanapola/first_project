from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('add-product-wishlist/', views.wishlistAddProductToWishlistCreateAPiView.as_view(), name = 'wishlistAddProductToWishlistCreateAPiViewURL'),
    path('get-all-wishlist/', views.wishlistGetAllWishlistDetailsListAPIView.as_view(), name = 'wishlistGetAllWishlistDetailsListAPIViewURL'),
    path('get-all-wishlist-id/<int:id>/', views.wishlistUserWishlistByIdDetailsListAPIView.as_view(), name = 'wishlistUserWishlistByIdDetailsListAPIViewURL'),

    ]