from easy_pdf.rendering import render_to_pdf

from .callsumo_report import CallSumoReport
from .jotform_report import JotFormReport


class OfficeReport:
    """
        Class  to get a whole office report,
        including callsumo and jotform reports
    """

    def __init__(self, account_id=None, office_name=None,
                 start_date=None, end_date=None):
        """
            :param account_id: CTM account id
            :param office_name: CTM  office name
            :param start_date: this is the date from when it generates the report
            :param end_date: this is the date until when  it generates the report
        """
        self.account_id = account_id
        self.office_name = office_name
        self.start_date = start_date
        self.end_date = end_date

    def callsumo_report(self):
        """
            Returns callsumo report containing new patients by source.

            :returns: dict containing callsumo report
        """

        callsumo = CallSumoReport(account_id=self.account_id)
        return callsumo.get_new_patients_by_source(
            self.start_date,
            self.end_date
        )

    def jotform_report(self, type='appointment'):
        """
            Returns jotform report given a form type (appointment or contact).

            :param type: This is the form type used for getting the report
                         it could be contact or appointment

            :returns: return a dict containing all submissions from a given dates
        """
        jotform = JotFormReport(office_name=self.office_name)
        return jotform.submissions_report(
            type,
            self.start_date,
            self.end_date
        )

    def report(self):
        """
            Returns report from callsumo new patients and all jotform reports type

            :returns: returns a dict containing callsumo and jotform reports
        """
        return {
            'callsumo': self.callsumo_report(),
            'jotform_appointment': self.jotform_report(
                type='Appointment'
            )
        }

    def send_report(self, email):
        """
            Sends a office report pdf to a given :param email:

            :param email: this is the email used to send the report
        """

        # Get pdf report
        pdf = self.pdf_report()

        # Send pdf file to a given email
        self.send_report(
            'levi@mrsft.com',
            pdf,
            'JotFormReport'
        )

    def pdf_report(self):
        """
            Creates a PDF file from report data returned from report()

            :returns: returns the pdf file created containing an office report
        """

        # Get data report
        data_report = self.report()

        # Create pdf containing report data
        pdf = render_to_pdf(
            'reports/new_patients.html',
            data_report,
        )

        return pdf
