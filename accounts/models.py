from django.db import models

from users.models import Profile
from users.roles import ROLES_CHOICES, ROLES_ACCESS_LEVEL


class Business(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(models.Model):
    call_metrics_id = models.IntegerField()
    name = models.CharField(max_length=100)
    business = models.ForeignKey(Business, related_name='accounts')
    profiles = models.ManyToManyField(Profile, through='Membership')

    def __str__(self):
        return "%s-%s" % (
            str(self.call_metrics_id),
            self.name
        )


class Membership(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES_CHOICES, max_length=40)

    def __str__(self):
        return "%s - %s - %s" % (
            self.profile.user.email,
            self.account.name,
            self.get_role_display()
        )

    @property
    def account_name(self):
        return self.account.name

    @property
    def role_name(self):
        return self.get_role_display()

    @classmethod
    def hasAccess(cls, profile, account_id, required_role):
        try:
            membership = Membership.objects.get(
                profile=profile,
                account__call_metrics_id=account_id
            )
        except Membership.DoesNotExist:
            return False

        current_role = membership.role
        return True if ROLES_ACCESS_LEVEL.get(current_role) >=\
            ROLES_ACCESS_LEVEL.get(required_role)\
            else False
