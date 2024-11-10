from django.urls import path
from .views import login_view, logout_view, sign_up_view, change_password_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('sing-up/', sign_up_view, name='sign-up'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change-password')
]
