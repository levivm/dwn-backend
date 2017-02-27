from django.conf.urls import url

from .views import CallsGetCreateView, CallsSaleUpdateView, CallAudioView, CallsTagView
urlpatterns = [

    # calls:accounts_tags - api/accounts/:account_id/tags
    url(
        regex=r'^(?P<account_id>\d+)/tags/?$',
        view=CallsTagView.as_view(),
        name='accounts_tags'
    ),


    # calls:accounts_calls - api/accounts/:account_id/calls
    url(
        regex=r'^(?P<account_id>\d+)/calls/?$',
        view=CallsGetCreateView.as_view(),
        name='accounts_calls'
    ),
    # calls:accounts_calls_edit - api/accounts/:account_id/calls/:call_id/
    url(
        regex=r'^(?P<account_id>\d+)/calls/(?P<call_id>\d+)/?$',
        view=CallsGetCreateView.as_view(),
        name='accounts_calls_edit'
    ),
    # calls:accounts_calls_sale_edit - api/accounts/:account_id/calls/:call_id/sale
    url(
        regex=r'^(?P<account_id>\d+)/calls/(?P<call_id>\d+)/sale/?$',
        view=CallsSaleUpdateView.as_view(),
        name='accounts_calls_sale_edit'
    ),
    # calls:accounts_calls_audio - api/accounts/:account_id/calls/:call_id/audio
    url(
        regex=r'^(?P<account_id>\d+)/calls/(?P<call_sid>[0-9A-Za-z]+)/audio/?$',
        view=CallAudioView.as_view(),
        name='accounts_calls_audio'
    ),
]
