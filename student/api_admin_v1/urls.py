from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('create-student/', views.studentCreateStudentGenericView.as_view(), name='studentCreateStudentGenericViewURL'),
    path('get-students/', views.studentGetAllStudentsListAPIView.as_view(), name='studentGetAllStudentsListAPIViewURL'),
    path('add-marks/', views.studentAddMarksToStudentGenericView.as_view(), name='studentAddMarksToStudentGenericViewURL'),
    # path('get-all-marks/<int:id>/', views.studentGetAllStudentsMarksListAPIView.as_view(), name='studentGetAllStudentsMarksListAPIViewURL'),
    path('get-all-marks-By-Id/<int:id>/', views.studentGetAllStudentsMarksByIdListAPIView.as_view(), name='studentGetAllStudentsMarksByIdListAPIViewURL'),
]