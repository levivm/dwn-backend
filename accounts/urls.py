from django.conf.urls import url

from .views import AccountsViewSet, AccountCalls

urlpatterns = [
    # auth:login - api/accounts/
    url(
        regex=r'^/?$',
        view=AccountsViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='accounts'
    ),
    # auth:login - api/accounts/:account_id/calls
    url(
        regex=r'^(?P<account_id>\d+)/calls/?$',
        view=AccountCalls.as_view(),
        name='accounts_calls'
    ),
    # auth:login - api/accounts/:account_id/calls/:call_id/
    url(
        regex=r'^(?P<account_id>\d+)/calls/(?P<call_id>\d+)/?$',
        view=AccountCalls.as_view(),
        name='accounts_calls_edit'
    ),
]
