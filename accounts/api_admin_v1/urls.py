from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name='token_refresh'),
    path('create-user/', views.accountsCreateUserCreateAPiView.as_view(), name = 'accountsCreateUserCreateAPiViewURL'),
    path('get-all-users/', views.accountsGetAllUserDetailsListAPIView.as_view(), name = 'accountsGetAllUserDetailsListAPIViewURLS'),
    path('send-otp/', views.accountsSendOtpCreateApiView.as_view(), name = 'accountsSendOtpCreateApiViewURL'),
    path('login-otp/', views.accountsLoginWithOtpCreateApiView.as_view(), name = 'accountsLoginWithOtpCreateApiViewURL'),
    # path('get-all-user-cart/', views.accountsGetAllUserCartDetailsListAPIView.as_view(), name = 'accountsGetAllUserCartDetailsListAPIViewURL'),
    # path('get-user-cart-id/<int:id>/', views.accountsUserCartByIdDetailsListAPIView.as_view(), name = 'accountsUserCartByIdDetailsListAPIViewURL'),

]