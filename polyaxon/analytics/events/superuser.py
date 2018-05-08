import analytics
from libs.event_manager.base_events import superuser

analytics.register(superuser.SuperUserRoleGrantedEvent)
analytics.register(superuser.SuperUserRoleRevokedEvent)
