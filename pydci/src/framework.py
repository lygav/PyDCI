import inspect

__all__ = ['Role', 'Context', 'StageProp']


def _role_hash(self):
    return self.__ob__.__hash__()


class Role(object):
    @property
    def context(self):
        """
        :return: The Context Object
        """
        return self.context

    def __new__(cls, ob, ctx, **kwargs):
        ob = ob.__ob__ if (isinstance(ob, Role) or isinstance(ob, StageProp)) else ob
        members = dict(__ob__=ob, context=ctx)
        c = type("{} as {}.{}".format(ob.__class__.__name__, cls.__module__, cls.__name__),
                 (cls, ob.__class__),
                 members)
        i = object.__new__(c)
        if hasattr(ob, '__dict__'):
            i.__dict__ = ob.__dict__
        return i

    def __init__(self, ob, ctx):
        pass

    __hash__ = _role_hash

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        return getattr(self.__ob__, attr)

    def __delattr__(self, item):
        delattr(self.__ob__, item)

    def __setattr__(self, name, value):
        assert hasattr(self.__ob__,
                       name), "{} trying to set non-existing attribute of name '{}'.Roles should be stateless.".format(
            self.__class__.__name__, name)
        setattr(self.__ob__, name, value)


class StageProp(object):
    @property
    def context(self):
        """
        :return: The Context Object
        """
        return self.context

    def __new__(cls, ob, ctx, **kwargs):
        ob = ob.__ob__ if (isinstance(ob, Role) or isinstance(ob, StageProp)) else ob
        members = dict(__ob__=ob, context=ctx)
        c = type("{} as {}.{}".format(ob.__class__.__name__, cls.__module__, cls.__name__),
                 (cls, ob.__class__),
                 members)
        i = object.__new__(c)
        if hasattr(ob, '__dict__'):
            super(StageProp, i).__setattr__('__dict__', ob.__dict__)
        return i

    def __init__(self, ob, ctx):
        pass

    __hash__ = _role_hash

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        return getattr(self.__ob__, attr)

    def __delattr__(self, item):
        self.__setattr__(item, None)

    def __setattr__(self, name, value):
        raise AttributeError('Trying to modify attribute {} of StageProp obj {}'.format(name, self))


class RoleDescriptor(object):
    def __init__(self, role):
        self.role = role

    def __set__(self, ctx, value):
        self.role = self.role(value, ctx)

    def __get__(self, instance, owner):
        return self.role


class Context(object):
    def __new__(cls, *args, **kwargs):
        members = dict(__slots__=[])
        roles = []
        for n, a in cls.__dict__.items():
            if inspect.isclass(a) and (issubclass(a, Role) or issubclass(a, StageProp)):
                members['__slots__'].append(n)
                roles.append((n, a))
        c = type("Context of {}.{}".format(cls.__module__, cls.__name__), (cls,), members)
        for n, r in roles:
            setattr(c, n, RoleDescriptor(r))
        i = object.__new__(c)
        return i
