from django.urls import path
from . import views
from .api import DepartmentListAPI, DepartmentDetailAPI, EmployeeListAPI, EmployeeDetailAPI

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'core'

urlpatterns = [
    # Department URLs
    path('', views.HomeView.as_view(), name='home'),
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department-form'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),
    
    # Employee URLs
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    
    
    # API URLs
    path('api/departments/', DepartmentListAPI.as_view(), name='api-department-list'),
    path('api/departments/<int:pk>/', DepartmentDetailAPI.as_view(), name='api-department-detail'),
    path('api/employees/', EmployeeListAPI.as_view(), name='api-employee-list'),
    path('api/employees/<int:pk>/', EmployeeDetailAPI.as_view(), name='api-employee-detail'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]