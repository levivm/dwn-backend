from utils.permissions import hasAdminAccessLevel


class hasAdminAccessLevelOrCanUpdate(hasAdminAccessLevel):

    def has_permission(self, request, view):
        is_same_user = False
        if request.method == 'PUT':
            profile_id = int(view.kwargs.get('pk'))
            is_same_user = request.user.profile.id == profile_id
            if is_same_user:
                return True

        return super(
            hasAdminAccessLevelOrCanUpdate,
            self
        ).has_permission(
            request,
            view,
        )
