from utils.mailer import ReportEmail


class ReportByEmailMixin:

    @classmethod
    def send_reports(cls, emails, pdf_reports):

        email_data = {
            'subject': 'Report',
            'to': emails,
            'context': {},
            'body': 'report',
        }

        email = ReportEmail(**email_data)
        email.set_attachments(
            files=pdf_reports,
        )
        email.send()
