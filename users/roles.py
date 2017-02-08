from rolepermissions.roles import AbstractUserRole


class Manager(AbstractUserRole):
    available_permissions = {
        'edit_call_record': True,
    }


class Viewer(AbstractUserRole):
    available_permissions = {
        'edit_call_record': True,
    }


class AgencyAdmin(AbstractUserRole):
    available_permissions = {
        'edit_call_record': True,
    }
