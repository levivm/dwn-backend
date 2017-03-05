from django.conf.urls import url

from .views import AccountsViewSet, AvailableAdminAccountsView, AccountSourcesView,\
    AccountReportsView

urlpatterns = [
    # accounts:accounts - api/accounts/
    url(
        regex=r'^/?$',
        view=AccountsViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='accounts'
    ),

    # accounts:accounts_sources - api/accounts/:account_id/sources
    url(
        regex=r'^(?P<account_id>\d+)/sources/?$',
        view=AccountSourcesView.as_view(),
        name='accounts_sources'
    ),

    # accounts:accounts_reports - api/accounts/:account_id/reports/series
    url(
        regex=r'^(?P<account_id>\d+)/reports/series/?$',
        view=AccountReportsView.as_view(),
        name='accounts_reports'
    ),

    # accounts:available_admin_accounts - api/accounts/available
    url(
        regex=r'^admin/?$',
        view=AvailableAdminAccountsView.as_view(),
        name='available_admin_accounts'
    ),
]
