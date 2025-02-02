from django.urls import path, include   
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('sign-up/', views.RegisterView.as_view(), name='register'),
    path('sign-up-confirmation/', views.ConfirmRegistrationView.as_view(), name='sign-up-confirmation'),
    path('sign-in/', views.LoginView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#    path('request-password-reset/', ratelimit(key='ip', rate='1/10m', method='POST', block=False)(RequestPasswordResetView.as_view()), name='request-password-reset'),
#     path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
]
