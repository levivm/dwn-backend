from django.conf.urls import url

from .views import AccountsViewSet, AvailableAdminAccountsView

urlpatterns = [
    # accounts:accounts - api/accounts/
    url(
        regex=r'^/?$',
        view=AccountsViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='accounts'
    ),
    # accounts:available_admin_accounts - api/accounts/available
    url(
        regex=r'^admin/?$',
        view=AvailableAdminAccountsView.as_view(),
        name='available_admin_accounts'
    ),
]
