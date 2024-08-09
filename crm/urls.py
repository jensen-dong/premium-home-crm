from django.urls import path, include
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/edit/<int:pk>/', views.client_update, name='client_update'),
    path('clients/delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('clients/<int:client_id>/pipeline/', views.sales_pipeline, name='sales_pipeline'),
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]