from django.db import models

from users.models import Profile


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

    ROLES_CHOICES = (
        ('admin', 'Administrator'),
        ('report_manager', 'Report Manager'),
        ('call_manager', 'Call Manager'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES_CHOICES, max_length=40)
