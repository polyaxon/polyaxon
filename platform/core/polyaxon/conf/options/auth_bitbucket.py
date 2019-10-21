import conf

from options.registry import auth_bitbucket

conf.subscribe(auth_bitbucket.AuthBitbucketEnabled)
conf.subscribe(auth_bitbucket.AuthBitbucketVerificationSchedule)
conf.subscribe(auth_bitbucket.AuthBitbucketClientId)
conf.subscribe(auth_bitbucket.AuthBitbucketClientSecret)
