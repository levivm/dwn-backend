from django.core.management.base import BaseCommand

from utils.ctm import CTMAPI

from accounts.models import Business, Account


class Command(BaseCommand):
    help = 'Fetch accounts from CTM API'

    def handle(self, *args, **options):
        ctm_api = CTMAPI()
        response = ctm_api.get_all_accounts()
        # business = []
        # accounts = []
        for account_data in response.get('accounts'):
            business, created = Business.objects.get_or_create(
                name=account_data.get('name')
            )
            account, created = Account.objects.get_or_create(
                call_metrics_id=account_data.get('id'),
                defaults={
                    'name': account_data.get('name'),
                    'business': business
                }
            )
