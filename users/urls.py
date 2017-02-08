from django.conf.urls import url

from .views import ProfileViewSet


urlpatterns = [
    # auth:login - api/accounts/
    url(
        regex=r'^/?$',
        view=ProfileViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users'
    ),
]
