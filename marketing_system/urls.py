"""
URL configuration for marketing_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from marketing_app.hrms_auth_views import hrms_login, hrms_logout, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    # HRMS RBAC Authentication
    path('hrms-login/', hrms_login, name='hrms_login'),
    path('hrms-logout/', hrms_logout, name='hrms_logout'),
    path('profile/', user_profile, name='user_profile'),
    # Legacy login (redirects to HRMS login)
    path('login/', auth_views.LoginView.as_view(template_name='marketing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('marketing_app.urls')),  # Marketing app handles all routes
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
