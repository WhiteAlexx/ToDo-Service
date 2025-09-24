from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from users import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
]
