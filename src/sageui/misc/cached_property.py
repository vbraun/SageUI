"""
A read-only cached version of @property
"""


class cached_property(object):

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, instance, cls):
        if instance is None:
            return self
        result = self.method(instance)
        setattr(instance, self.name, result)
        return result
