from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path("settings/security/", views.security, name="security_settings"),
    path("forgot/", views.forgot_password_start, name="forgot_password_start"),
    path("forgot/verify/", views.forgot_password_verify, name="forgot_password_verify"),
]