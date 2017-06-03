import calendar
import datetime

from easy_pdf.rendering import render_to_pdf

from utils.ctm import CTMAPI

from .callsumo_report import CallSumoReport
from .jotform_report import JotFormReport
from .mixins import ReportByEmailMixin


class OfficeReport(ReportByEmailMixin):
    """
        Class  to get a whole office report,
        including callsumo and jotform reports
    """

    ctm_api = CTMAPI()

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
        self.report_data = {
            'office_name': self.office_name,
            'from_date': self.start_date,
            'to_date': self.end_date,
            'callsumo': self.callsumo_report(),
            'jotform_appointment': self.jotform_report(
                type='Appointment'
            ),
        }

        return self.report_data

    def send_report_by_email(self, emails=None):
        """
            Sends a office pdf report to a given :param email:

            :param email: this is the email used to send the report
        """

        # Get pdf report
        pdf = self.pdf_report()
        pdf_report = {
            self.office_name: pdf
        }
        # Send pdf file to a given email
        self.send_reports(
            emails,
            pdf_report,
            'MonthlyReport'
        )

    def pdf_report(self):
        """
            Creates a PDF file from report data returned from report()

            :returns: returns the pdf file created containing an office report
        """

        # Get data report
        data_report = self.report()
        print('office', self.office_name)
        import pprint
        pprint.pprint(data_report)

        # Create pdf containing report data
        pdf = render_to_pdf(
            'reports/new_patients.html',
            data_report,
        )

        return pdf

    @classmethod
    def send_monthly_reports(cls):
        # Get today date
        today = datetime.datetime.today()

        # Get how many days has the current month
        months_days = calendar.monthrange(
            today.year,
            today.month
        )[1]

        # Date representing the first day of the current month
        first_day_month_date = datetime.date(
            today.year,
            today.month,
            1
        )

        # Convert date to string
        first_day_month = first_day_month_date.strftime("%Y-%d-%m")

        # Date representing the last day of the current month
        last_day_month_date = first_day_month_date + datetime.timedelta(
            days=(months_days - 1)
        )

        # Convert date to string
        last_day_month = last_day_month_date.strftime("%Y-%d-%m")

        # Get all accounts from CTM API
        accounts_data = cls.ctm_api.get_all_accounts()
        accounts = accounts_data.get('accounts')

        # Init an empty pdf report list
        pdf_reports = {}

        # For each account, generate it's report and then appending it
        # to pdf reports list
        for account in accounts:
            office_name = account.get('name')
            account_id = account.get('id')

            if account_id not in [75367, 99878]:
                continue

            # Generate the report
            report = cls(
                account_id=account_id,
                office_name=office_name,
                start_date=first_day_month,
                end_date=last_day_month,
            )

            # Get pdf file from report data
            pdf = report.pdf_report()

            # Append gotten report to pdf reports list
            pdf_reports.update({
                office_name: pdf
            })

        # Send pdf reports to a list of given emails
        cls.send_reports(
            ['levi@mrsft.com'],
            pdf_reports
        )
