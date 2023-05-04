
from django.urls import path
from . import views
urlpatterns = [
    path('sign_up',views.sign_up),
    path('email_check',views.email_check),
    path('admin_login',views.admin_login),
    path('user_login',views.user_login),
]