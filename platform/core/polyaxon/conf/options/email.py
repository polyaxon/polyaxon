import conf

from options.registry import email

conf.subscribe(email.EmailDefaultDomain)
conf.subscribe(email.DefaultFromEmail)
conf.subscribe(email.EmailHostUser)
conf.subscribe(email.EmailHostPassword)
