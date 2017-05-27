from django.conf.urls import url

from .views import (
    FindNumbersView,
    TrackingNumbersView,
    ReceivingNumbersView,
    TrackingNumbersRoutesView
)

urlpatterns = [

    # numbers:find - api/accounts/:account_id/numbers/search
    url(
        regex=r'^(?P<account_id>\d+)/numbers/search/?$',
        view=FindNumbersView.as_view(),
        name='find'
    ),
    # numbers:receiving_numbers - api/accounts/:account_id/receiving_numbers/
    url(
        regex=r'^(?P<account_id>\d+)/receiving_numbers/?$',
        view=ReceivingNumbersView.as_view(),
        name='receiving_numbers'
    ),
    # numbers:tracking_numbers - api/accounts/:account_id/tracking_numbers/
    url(
        regex=r'^(?P<account_id>\d+)/tracking_numbers/?$',
        view=TrackingNumbersView.as_view(),
        name='tracking_numbers'
    ),
    # numbers:tracking_numbers_routes -api/accounts/:account_id/numbers/:tracking_number_id/routes
    url(
        regex=r'^(?P<account_id>\d+)/tracking_numbers/(?P<tracking_number_id>\w+)/routes?$',
        view=TrackingNumbersRoutesView.as_view(),
        name='tracking_numbers_routes'
    ),

]
