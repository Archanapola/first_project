from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('create-vehicle/', views.vehicleCreateVehicleGenericView.as_view(), name = 'vehicleCreateVehicleGenericViewURL'),
    path('get-all-vehicles/', views.vehicleGetAllVehiclesListAPIView.as_view(), name = 'vehicleGetAllVehiclesListAPIViewURL'),
    path('breakdown-with-image/', views.vehicleBreakdownWithImageGenericView.as_view(), name = 'vehicleBreakdownWithImageGenericViewURL'),
    path('breakdown-details/', views.VehicleBreakdownDetailsAPIView.as_view(), name = 'vehicleBreakdownWithImageGenericViewURL'),
    path('assign-bd-user/', views.vehicleAssignBreakdownToUserCreateAPIView.as_view(), name = 'vehicleAssignBreakdownToUserCreateAPIViewURL'),
    path('inspection-with-image/', views.vehicleInspectionWithImageGenericView.as_view(), name = 'vehicleInspectionWithImageGenericViewURL'),
    # path('repair-with-image/', views.vehicleRepairWithImageGenericView.as_view(), name='vehicleRepairWithImageGenericViewURL'),
    path('get-all-breakdown-details/<int:id>/', views.vehicleGetAllBreakdownDetailsByIdListView.as_view(), name='vehicleGetAllBreakdownDetailsByIdListViewURL'),

]