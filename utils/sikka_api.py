import requests


class SikkaAPI():

    SIKKA_AUTH_HOST = 'https://api.sikkasoft.com/auth/v2/'
    SIKKA_HOST = 'https://api.sikkasoft.com/v2/'
    APP_ID = 'f3fe40f14afb2a54866e6ebfa55ceac5'
    APP_KEY = 'afe925eaa894b73cbaa553b3ec231ecb'

    def get(self, endpoint, host):

        host = self.SIKKA_HOST if host is None else host

        url = "%s%s" % (
            host,
            endpoint
        )

        response = requests.get(url)
        return response.json()

    def get_practices(self):

        # Set queryparams for get authorized practices
        queryparams = "app_id=%s&app_key=%s" % (
            self.APP_ID,
            self.APP_KEY
        )

        # Set endpoint for get authorized practices
        endpoint = 'authorized_practices?%s' % (queryparams)

        return self.get(endpoint, self.SIKKA_AUTH_HOST)
