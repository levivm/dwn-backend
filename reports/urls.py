from django.conf.urls import url

from .views import NewPatientsReportView, JotFormSubmissionsReportView


urlpatterns = [
    # reports:new_patients - api/reports/new_patients
    url(
        regex=r'^new_patients/?$',
        view=NewPatientsReportView.as_view(),
        name='new_patients'
    ),
    # reports:jotform - api/reports/jotform/appointments
    url(
        regex=r'^jotform/?$',
        view=JotFormSubmissionsReportView.as_view(),
        name='jotform'
    ),

]
