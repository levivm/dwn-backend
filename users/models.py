from django.db import models
from django.contrib.auth.models import User

from utils.mixins import UpdateableMixin


# Create your models here.

class Profile(UpdateableMixin, models.Model):
    user = models.OneToOneField(User, related_name='profile')
    telephone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    agency_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    @classmethod
    def generate_username(cls, first_name, last_name):
        username = '%s.%s' % (first_name.lower(), last_name.lower())
        username = '{:.25}'.format(username)
        counter = User.objects.filter(first_name=first_name, last_name=last_name).count()
        if counter > 0:
            username += '%s' % (counter + 1)
        print(username)
        return username

    def update_user(self, data):
        Profile.update_related_model(self.user, data)
