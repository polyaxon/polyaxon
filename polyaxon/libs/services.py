import inspect
import itertools
import logging

from django.utils.functional import empty, LazyObject

from libs.imports import import_string


logger = logging.getLogger(__name__)


class InvalidService(Exception):
    pass


class Service(object):
    __all__ = ()

    def validate(self):
        """Validate the settings for this backend (i.e. such as proper connection info).

        Raise ``InvalidService`` if there is a configuration error.
        """

    def setup(self):
        """Initialize this service."""


class EventService(Service):
    __all__ = ('record', 'validate')

    event_manager = None
    EventModel = None

    def record(self, event_or_event_type, instance=None, **kwargs):
        """
        >>> record(Event())
        >>> record('event.action', object_instance)
        """
        if isinstance(event_or_event_type, str):
            event = self.event_manager.get(
                event_or_event_type,
            ).from_instance(instance, **kwargs)
        elif isinstance(event_or_event_type, self.EventModel):
            event = event_or_event_type.from_instance(instance, **kwargs)
        else:
            return
        self.record_event(event)

    def record_event(self, event):
        """
        >>> record_event(Event())
        """
        pass


class LazyServiceWrapper(LazyObject):
    """Lazyily instantiates a Polyaxon standard service class.

    >>> LazyServiceWrapper(BaseClass, 'path.to.import.Backend', {})

    Provides an ``expose`` method for dumping public APIs to a context, such as module locals:

    >>> service = LazyServiceWrapper(...)
    >>> service.expose(locals())
    """

    def __init__(self, backend_base, backend_path, options):
        super(LazyServiceWrapper, self).__init__()
        self.__dict__.update(
            {
                '_backend_base': backend_base,
                '_backend_path': backend_path,
                '_options': options,
            }
        )

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup()
        return getattr(self._wrapped, name)

    def _setup(self):
        backend = import_string(self._backend_path)
        assert issubclass(backend, Service)
        instance = backend(**self._options)
        self._wrapped = instance

    def expose(self, context):
        base = self._backend_base
        for key in itertools.chain(base.__all__, ('validate', 'setup')):
            if inspect.ismethod(getattr(base, key)):
                context[key] = (lambda f: lambda *a, **k: getattr(self, f)(*a, **k))(key)
            else:
                context[key] = getattr(base, key)
