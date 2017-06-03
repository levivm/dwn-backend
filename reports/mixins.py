from utils.mailer import ReportEmail


class ReportByEmailMixin:

    def send_report(self, emails, pdf_report, name):

        email_data = {
            'subject': 'Report',
            'to': emails,
            'context': {},
            'body': 'report',
        }

        email = ReportEmail(**email_data)
        email.set_attachment(
            file=pdf_report,
            name=name
        )
        email.send()
