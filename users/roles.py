AGENCY_ADMIN = 'agency_admin'
ADMIN_ROLE = 'admin'
REPORT_MANAGER_ROLE = 'report_manager'
CALL_MANAGER_ROLE = 'call_manager'


AGENCY_ADMIN_DISPLAY = 'Agency Admin'

ROLES_ACCESS_LEVEL = {
    AGENCY_ADMIN: 4,
    ADMIN_ROLE: 3,
    REPORT_MANAGER_ROLE: 2,
    CALL_MANAGER_ROLE: 1
}

ROLES_CHOICES = (
    (ADMIN_ROLE, 'Administrator'),
    (REPORT_MANAGER_ROLE, 'Report Manager'),
    (CALL_MANAGER_ROLE, 'Call Manager'),
)
