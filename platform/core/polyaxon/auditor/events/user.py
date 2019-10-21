import auditor

from events.registry import user

auditor.subscribe(user.UserRegisteredEvent)
auditor.subscribe(user.UserUpdatedEvent)
auditor.subscribe(user.UserActivatedEvent)
auditor.subscribe(user.UserDeletedEvent)
auditor.subscribe(user.UserLDAPEvent)
auditor.subscribe(user.UserGITHUBEvent)
auditor.subscribe(user.UserGITLABEvent)
auditor.subscribe(user.UserBITBUCKETEvent)
auditor.subscribe(user.UserAZUREEvent)
