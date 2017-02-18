from django.conf.urls import url

from .views import LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    # auth:login - api/auth/login
    url(
        regex=r'^login/?$',
        view=LoginView.as_view(),
        name='login'
    ),
    # auth:forgot_password - api/auth/reset-forgot_password
    url(
        regex=r'^forgot-password/?$',
        view=ForgotPasswordView.as_view(),
        name='forgot_password'
    ),
    # auth:reset_password - api/auth/reset-password
    url(
        regex=r'^reset-password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/?$',
        view=ResetPasswordView.as_view(),
        name='reset_password'
    ),
]
