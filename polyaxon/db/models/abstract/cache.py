class CachedMixin(object):
    """
    A mixin to help clear cached properties.
    """
    CACHED_PROPERTIES = ()

    def clear_cached_properties(self, properties=None):
        properties = properties or self.CACHED_PROPERTIES
        for key in properties:
            if key in self.__dict__:
                del self.__dict__[key]
