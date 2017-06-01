from easy_pdf.rendering import render_to_pdf

from .callsumo_report import CallSumoReport
from .jotform_report import JotFormReport


class OfficeReport:

    def __init__(self, account_id=None, office_name=None,
                 start_date=None, end_date=None):
        self.account_id = account_id
        self.office_name = office_name
        self.start_date = start_date
        self.end_date = end_date

    def callsumo_report(self):
        callsumo = CallSumoReport(account_id=self.account_id)
        return callsumo.get_new_patients_by_source(
            self.start_date,
            self.end_date
        )

    def jotform_report(self, type='appointment'):
        jotform = JotFormReport(office_name=self.office_name)
        return jotform.submissions_report(
            type,
            self.start_date,
            self.end_date
        )

    def report(self):
        return {
            'callsumo': self.callsumo_report(),
            'jotform_appointment': self.jotform_report(
                type='Appointment'
            )
        }

    def pdf_report(self, start_date,):
        data_report = self.report()
        pdf = render_to_pdf(
            'reports/new_patients.html',
            data_report,
        )
        self.send_report(
            'levi@mrsft.com',
            pdf,
            'JotFormReport'
        )
        return pdf
