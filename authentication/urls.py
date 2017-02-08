from django.conf.urls import url

from .views import LoginView

urlpatterns = [
    # auth:login - api/auth/login
    url(
        regex=r'^login/?$',
        view=LoginView.as_view(),
        name='login'
    ),
]
