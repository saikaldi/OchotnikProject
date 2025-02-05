from django.urls import path, include   
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('sign-up/', views.RegisterView.as_view(), name='register'),
    path('sign-up-confirmation/', views.ConfirmRegistrationView.as_view(), name='sign-up-confirmation'),
    path('sign-in/', views.LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
    path('request-password-reset/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('confirm-password-reset/', views.ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
 ]
