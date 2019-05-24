import conf

from options.registry import ownership

conf.subscribe(ownership.AllowUserProjects)
conf.subscribe(ownership.OwnerTypes)
conf.subscribe(ownership.Roles)
conf.subscribe(ownership.DefaultRole)
conf.subscribe(ownership.ScopeRoles)
