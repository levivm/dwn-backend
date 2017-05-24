from django.conf.urls import url

from .views import NewPatientsReportView


urlpatterns = [
    # reports:new_patients - api/reports/new_patients
    url(
        regex=r'^new_patients/?$',
        view=NewPatientsReportView.as_view(),
        name='new_patients'
    ),
]
