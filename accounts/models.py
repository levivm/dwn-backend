from django.db import models

from users.models import Profile
from users.roles import ROLES_CHOICES


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
        return str(self.call_metrics_id)


class Membership(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES_CHOICES, max_length=40)

    @property
    def account_name(self):
        return self.account.name

    @property
    def role_name(self):
        return self.get_role_display()
