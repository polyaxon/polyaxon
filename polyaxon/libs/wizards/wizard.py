from django.shortcuts import render_to_response

from libs.hashing import md5_text
from libs.redis_db import RedisSessions


class Wizard(object):
    """The Wizard provides a mechanism to guide the user through a wizard of requests.

    The wizard works with a WizardProvider object which provides the views
    an is also made available to the views.

    Params:
        * manager: A class property that must be specified to allow for lookup of a provider
        implementation object given it's key.

        * model_cls: The Provider model object represents the instance of an object implementing
        the WizardProvider interface.

        * config: A object that specifies additional context and provider runtime configurations.
    """
    name = None
    manager = None
    model_cls = None

    @classmethod
    def get_for_request(cls, request):
        state = RedisSessions(request, cls.name)
        if not state.is_valid():
            return None

        provider_model = None
        if state.provider_model_id:
            provider_model = cls.model_cls.objects.get(id=state.provider_model_id)

        provider_key = state.provider_key
        config = state.config

        return cls(request, provider_key, provider_model, config)

    def __init__(self, request, provider_key, provider_model=None, config=None):
        self.request = request
        self.state = RedisSessions(request, self.name)
        self.provider = self.manager.get(provider_key)()
        self.provider_model = provider_model

        self.config = config or {}
        self.provider.set_config(self.config)

        self.wizard = self.get_wizard_views()

        # we serialize the wizard to be ['fqn.WizardView', ...] which
        # allows us to determine if the wizard has changed during the auth
        # flow or if the user is somehow circumventing a chunk of it
        pipe_ids = ['{}.{}'.format(type(v).__module__, type(v).__name__) for v in self.wizard]
        self.signature = md5_text(*pipe_ids).hexdigest()

    def get_wizard_views(self):
        """Retrieve the wizard views from the provider."""
        return self.provider.get_wizard_views()

    def is_valid(self):
        return self.state.is_valid() and self.state.signature == self.signature

    def initialize(self):
        self.state.regenerate({
            'user_id': self.request.user.id if self.request.user.is_authenticated else None,
            'provider_model_id': self.provider_model.id if self.provider_model else None,
            'provider_key': self.provider.key,
            'step_index': 0,
            'signature': self.signature,
            'config': self.config,
            'data': {},
        })

    def clear_session(self):
        self.state.clear()

    def current_step(self):
        step_index = self.state.step_index

        if step_index == len(self.wizard):
            return self.finish_wizard()

        return self.wizard[step_index].dispatch(
            request=self.request,
            wizard=self,
        )

    def error(self, message):
        context = {'error': message}
        return render_to_response('polyaxon/wizard_error.html', context, self.request)

    def next_step(self):
        self.state.step_index += 1
        return self.current_step()

    def finish_wizard(self):
        raise NotImplementedError

    def bind_state(self, key, value):
        data = self.state.data
        data[key] = value

        self.state.data = data

    def fetch_state(self, key=None):
        return self.state.data if key is None else self.state.data.get(key)
