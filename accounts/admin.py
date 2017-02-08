from django.contrib import admin

from .models import Account, Business, Membership

admin.site.register(Account)
admin.site.register(Business)
admin.site.register(Membership)

# Register your models here.
