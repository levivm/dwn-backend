from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BaseEmail(object):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.get('to')
        self.template_name = kwargs.get('template_name')
        self.template_path = kwargs.get('template_path')
        self.subject = kwargs.get('subject')
        self.context = kwargs.get('context', {})
        self.template_full_path = '%s%s' % (self.template_path, self.template_name)
        text_content = render_to_string('%s.txt' % self.template_full_path, self.context)
        html_content = render_to_string('%s.html' % self.template_full_path, self.context)

        self.email = EmailMultiAlternatives(self.subject, text_content)
        self.email.attach_alternative(html_content, "text/html")
        self.email.from_email = '(Dental Web Now) DWN Support <levi@mrsft.com>'
        self.email.to = [kwargs.get('to', 'levi@mrsft.com')]

    def send(self):
        self.email.send()
