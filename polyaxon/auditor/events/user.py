import auditor

from event_manager.events import user

auditor.subscribe(user.UserRegisteredEvent)
auditor.subscribe(user.UserUpdatedEvent)
auditor.subscribe(user.UserActivatedEvent)
auditor.subscribe(user.UserDeletedEvent)
auditor.subscribe(user.UserLDAPEvent)
auditor.subscribe(user.UserGITHUBEvent)
auditor.subscribe(user.UserGITLABEvent)
auditor.subscribe(user.UserBITBUCKETEvent)
