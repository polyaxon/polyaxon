import auditor
from libs.event_manager.base_events import superuser

auditor.register(superuser.SuperUserRoleGrantedEvent)
auditor.register(superuser.SuperUserRoleRevokedEvent)
