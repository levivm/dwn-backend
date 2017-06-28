from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from utils.ctm import CTMAPI
from users.models import Profile
from accounts.models import Account, Membership


class Command(BaseCommand):
    help = 'Run the tasks for calculate balance'

    def handle(self, *args, **options):
        ctm_api = CTMAPI()
        accounts = Account.objects.all()

        for account in accounts:

            users_data = ctm_api.get_all_users(account.call_metrics_id)

            for user_data in users_data:

                first_name, last_name = [
                    user_data.get('first_name'),
                    user_data.get('last_name')
                ]
                username = Profile.generate_username(
                    first_name,
                    last_name
                )
                email = user_data.get('email')
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username
                    }
                )

                if not created:

                    Token.objects.get_or_create(user=user)

                    user.set_password('%spassword' % email)
                    user.save()

                role = user_data.get('role')
                profile, created = Profile.objects.get_or_create(
                    user=user
                )

                Membership.objects.get_or_create(
                    profile=profile,
                    role=role,
                    account=account
                )
