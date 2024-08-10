from django.urls import path
from . import views
from .views import redirect_to_appropriate_view

urlpatterns = [
    path('', redirect_to_appropriate_view, name='root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Client Management
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/edit/<int:pk>/', views.client_update, name='client_update'),
    path('clients/delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('clients/<int:client_id>/pipeline/', views.sales_pipeline, name='sales_pipeline'),

    # Campaign Management
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/new/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:campaign_id>/send/', views.send_campaign, name='send_campaign'),

    # Lead Management
    path('leads/', views.lead_list, name='lead_list'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]