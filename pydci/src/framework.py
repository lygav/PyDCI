import inspect

__all__ = ['Role', 'Context', 'StageProp']

def _proxy_getattr(self, attr):
    if attr == 'context':
        return self.context
    return getattr(self.__ob__, attr)


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
        ob = ob.__ob__ if isinstance(ob, Role) else ob
        members = dict(__ob__=ob, context=ctx)
        if hasattr(ob.__class__, '__slots__'):
            members['__setattr__'] = Role.__proxy_setattr
            members['__getattr__'] = Role.__proxy_getattr
            members['__delattr__'] = Role.__proxy_delattr

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

    __proxy_getattr = _proxy_getattr

    def __proxy_setattr(self, attr, val):
        setattr(self.__ob__, attr, val)

    def __proxy_delattr(self, attr):
        delattr(self.__ob__, attr)

    def __setattr__(self, name, value):
        assert hasattr(self.__ob__,
                       name), "{} trying to set non-existing attribute of name '{}'.Roles should be stateless.".format(
            self.__class__.__name__, name)
        super(Role, self).__setattr__(name, value)


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
        members['__setattr__'] = StageProp.__proxy_setattr
        members['__getattr__'] = StageProp.__proxy_getattr
        members['__delattr__'] = StageProp.__proxy_delattr

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

    __proxy_getattr = _proxy_getattr

    def __proxy_setattr(self, attr, val):
        raise AttributeError('Trying to modify attribute {} of immutable StageProp obj {}'.format(attr, self))

    def __proxy_delattr(self, attr):
        self.__proxy_setattr(attr, None)

    def __setattr__(self, name, value):
        self.__proxy_setattr(name, None)


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