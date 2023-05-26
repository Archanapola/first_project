from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('create-product/', views.productCreateProductCreateAPiView.as_view(), name = 'productCreateProductCreateAPiViewURL'),
    path('get-products-images/', views.productGetAllUserProductsListAPIView.as_view(), name = 'productGetAllUserProductsListAPIViewURL'),
    path('create-product-images/', views.productCreateProductWithMultipleImagesCreateAPiView.as_view(), name = 'productCreateProductWithMultipleImagesCreateAPiViewURL'),
    path('add-product-cart/', views.productAddProductToCartCreateAPiView.as_view(), name = 'productAddProductToCartCreateAPiViewURL'),
    # path('add-product-wishlist/', views.productAddProductToWishlistCreateAPiView.as_view(), name = 'productAddProductToWishlistCreateAPiView'),
    path('get-all-user-cart/', views.productGetAllUserCartDetailsListAPIView.as_view(), name = 'productGetAllUserCartDetailsListAPIViewURL'),
    path('get-user-cart-id/<int:id>/', views.productUserCartByIdDetailsListAPIView.as_view(), name = 'productUserCartByIdDetailsListAPIViewURL'),


]