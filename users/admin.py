from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token

from accounts.models import Business, Membership

from .models import Profile
from .roles import ADMIN_ROLE


class ProfileAdminForm(forms.ModelForm):

    business = forms.ModelChoiceField(queryset=Business.objects.all(),
                                      widget=forms.Select())

    class Meta:
        model = Profile
        fields = ('telephone', 'agency_admin', 'business', 'user')

    def create_admin_memberships(self, business, profile):
        accounts = business.accounts.all()
        memberships = []
        for account in accounts:
            memberships += [Membership(profile=profile, account=account, role=ADMIN_ROLE)]
        Membership.objects.bulk_create(memberships)

    def save(self, commit=True):
        business = self.cleaned_data.get('business', None)
        agency_admin = self.cleaned_data.get('agency_admin', None)

        if self.instance.pk and not agency_admin:
            profile = super(ProfileAdminForm, self).save(commit=commit)
            profile.save()
            Membership.objects.filter(profile=profile, role=ADMIN_ROLE).delete()
            return profile

        # profile does not exists
        if not self.instance.pk:
            profile = super(ProfileAdminForm, self).save(commit=commit)
            profile.save()
            if business:
                self.create_admin_memberships(business, profile)
            return profile

        profile = self.instance
        self.create_admin_memberships(business, profile)
        return super(ProfileAdminForm, self).save(commit=commit)

    def __init__(self, *args, **kwargs):

        super(ProfileAdminForm, self).__init__(*args, **kwargs)

        # Avoid to change business to existing profile users
        if self.instance and self.instance.pk and self.instance.account_set.all():
            self.fields['business'].initial = self.instance.account_set.first().business.id
            self.fields['business'].disabled = True


class ProfileAdmin(admin.ModelAdmin):

    form = ProfileAdminForm

    fieldsets = (
        (None, {
            'fields': ('telephone', 'agency_admin', 'business', 'user'),
        }),
    )


# Extending User Form
class UserCreationFormExtended(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)
        # self.fields.pop('username')

    def save(self, commit=True):
        user = super(UserCreationFormExtended, self).save(commit=False)
        user.username = user.email
        user.save()
        Token.objects.get_or_create(user=user)
        return user


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.edit_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2')
    }),
)

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

