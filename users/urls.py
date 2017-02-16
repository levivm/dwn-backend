from django.conf.urls import url

from .views import ProfileViewSet, UsersRolesView


urlpatterns = [
    # users:list - api/accounts/:account_id/users
    url(
        regex=r'^(?P<account_id>\d+)/users/?$',
        view=ProfileViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='list'
    ),
    # users:list - api/accounts/:account_id/users/:user_id
    url(
        regex=r'^(?P<account_id>\d+)/users/(?P<pk>\d+)?$',
        view=ProfileViewSet.as_view({'put': 'update'}),
        name='list'
    ),

    # users:users_roles - api/accounts/users/roles
    url(
        regex=r'^users/roles/?$',
        view=UsersRolesView.as_view(),
        name='users_roles'
    ),
]
