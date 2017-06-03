from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BaseEmail(object):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.get('to')
        self.template_name = kwargs.get('template_name')
        self.template_path = kwargs.get('template_path')
        self.subject = kwargs.get('subject')
        self.context = kwargs.get('context', {})

        if self.template_name and self.template_path:
            self.template_full_path = '%s%s' % (self.template_path, self.template_name)
            text_content = render_to_string('%s.txt' % self.template_full_path, self.context)
            html_content = render_to_string('%s.html' % self.template_full_path, self.context)
        else:
            text_body = kwargs.get('body')
            text_content = text_body
            html_content = text_body

        self.email = EmailMultiAlternatives(self.subject, text_content)
        self.email.attach_alternative(html_content, "text/html")
        self.email.from_email = '(Dental Web Now) DWN Support <levi@mrsft.com>'
        self.email.to = kwargs.get('to', ['levi@mrsft.com'])

    def send(self):
        self.email.send()


class ReportEmail(BaseEmail):
    MIME_TYPE = 'application/pdf'

    def set_attachments(self, files=None):
        for name, file in files.items():
            self.email.attach(
                name,
                file,
                self.MIME_TYPE
            )
