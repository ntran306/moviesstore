from django.urls import path
from . import views

urlpatterns = [
    path('login/',  views.login,  name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('orders/', views.orders, name='orders'),

    path('settings/security/', views.security_settings, name='security_settings'),
    path('forgot/',          views.forgot_password_start,  name='forgot_password_start'),
    path('forgot/verify/',   views.forgot_password_verify, name='forgot_password_verify'),
]
