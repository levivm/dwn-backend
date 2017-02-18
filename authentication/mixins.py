from django.conf import settings


class PasswordResetLinkMixin():

    @classmethod
    def generate_reset_link(cls, uid, token):
        uid = uid.decode('utf-8')
        base_url = settings.FRONTEND_URL
        url = "{0}/auth/password/reset/{1}-{2}".format(base_url, uid, token)
        return url
