from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from rolepermissions.shortcuts import assign_role

from .models import Profile


class UserCreationFormExtended(UserCreationForm):

    ROLES_CHOICES = (
        ('manager', 'manager'),
        ('administrator', 'administrator')
    )

    role = forms.ChoiceField(choices=ROLES_CHOICES,
                             widget=forms.Select(), required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)

    def save(self, commit=True):
        user = super(UserCreationFormExtended, self).save(commit=False)
        user.save()
        # role = self.cleaned_data.get('role')
        # assign_role(user, role)
        Token.objects.get_or_create(user=user)
        return user


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'username', 'password1', 'password2', 'role')
    }),
)

admin.site.register(Profile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
