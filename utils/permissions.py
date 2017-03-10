from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from accounts.models import Membership
from users import roles


class hasAccessLevel(permissions.BasePermission):
    def has_permission(self, request, view, required_role):
        profile = request.user.profile
        account_id = view.kwargs.get('account_id')

        if not account_id:
            return True

        if profile.agency_admin:
            return True

        # required_role = roles.ADMIN_ROLE

        return Membership.hasAccess(
            profile,
            account_id,
            required_role
        )


class hasAdminAccessLevel(hasAccessLevel):

    def has_permission(self, request, view):
        required_role = roles.ADMIN_ROLE
        return super(
            hasAdminAccessLevel,
            self
        ).has_permission(
            request,
            view,
            required_role
        )


class hasReportManagerAccessLevel(hasAccessLevel):

    def has_permission(self, request, view):
        required_role = roles.REPORT_MANAGER_ROLE
        return super(
            hasReportManagerAccessLevel,
            self
        ).has_permission(
            request,
            view,
            required_role
        )
