from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('management/', views.user_management, name='user-management'),
    path('toggle-permission/<int:user_id>/', views.toggle_event_permission, name='toggle-event-permission'),
    path('edit-permissions/<int:user_id>/', views.edit_user_permissions, name='edit-user-permissions'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]