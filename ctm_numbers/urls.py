from django.conf.urls import url

from .views import (
    FindNumbersView,
    TrackingNumbersView,
    ReceivingNumbersView,
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
    # numbers:update_tracking_numbers - api/accounts/:account_id/tracking_numbers/
    url(
        regex=r'^(?P<account_id>\d+)/tracking_numbers/?$',
        view=TrackingNumbersView.as_view(),
        name='update_tracking_numbers'
    ),
    # numbers:buy_tracking_number - api/accounts/:account_id/numbers/
    url(
        regex=r'^(?P<account_id>\d+)/tracking_numbers/?$',
        view=TrackingNumbersView.as_view(),
        name='buy_tracking_number'
    ),

]
