from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('create-order/', views.orderCreateOrderAPiView.as_view(), name = 'orderCreateOrderAPiViewURL'),
    path('get-all-orders/', views.orderGetAllOrdersDetailsListAPIView.as_view(), name = 'orderGetAllOrdersDetailsListAPIViewURL'),
    path('order-update-status/<int:pk>/', views.orderUpdateStatusAPIView.as_view(), name = 'orderUpdateStatusAPIViewURL'),
    path('get-user-order/<int:id>/', views.orderGetUserOrdersListAPIView.as_view(), name = 'orderGetUserOrdersListAPIView'),

    ]