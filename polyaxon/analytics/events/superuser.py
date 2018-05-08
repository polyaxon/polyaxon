import analytics
from event_manager.events import superuser

analytics.register(superuser.SuperUserRoleGrantedEvent)
analytics.register(superuser.SuperUserRoleRevokedEvent)
