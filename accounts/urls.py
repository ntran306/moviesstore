from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('signup/', views.signup, name='accounts.signup'),
    path('orders/', views.orders, name='accounts.orders'),

    # security phrase flow
    path('settings/security/', views.security_settings, name='accounts.security_settings'),
    path('forgot/', views.forgot_password_start, name='accounts.forgot_password_start'),
    path('forgot/verify/', views.forgot_password_verify, name='accounts.forgot_password_verify'),
]
