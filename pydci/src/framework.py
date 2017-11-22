import inspect
from functools import wraps

__all__ = ['Role', 'Context', 'StageProp']


def _role_hash(self):
    return self.__ob__.__hash__()


def interceptor(fn, wrapped_name):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if hasattr(self.__ob__, wrapped_name):
            print(
                "WARNING: Both {!r} and {!r} classes contain same method {!r}. This can lead to unexpected behaviour.".format(
                    self.__class__.__name__, self.__ob__.__class__.__name__, wrapped_name))
        return fn(self, *args, **kwargs)

    wrapper.wrapped = True
    return wrapper


class RoleBase(object):
    @property
    def context(self):
        """
        :return: The Context Object
        """
        return self.context

    def __new__(role, ob, ctx=None, **kwargs):
        ob = ob.__ob__ if (isinstance(ob, Role) or isinstance(ob, StageProp)) else ob
        members = dict(__ob__=ob, context=ctx)

        namespace = dict()
        default = {'__getattr__', '__metaclass__'}.union(type.__dict__.keys())
        for n, m in inspect.getmembers(role):
            if (inspect.ismethod(m) or inspect.isfunction(m)) and n not in default:
                namespace[n] = interceptor(m, n)
        for n, m in inspect.getmembers(ob, lambda o: isinstance(o, Role)):
            members[n] = None

        role_base = type.__new__(type, role.__name__, (role,), namespace)

        c = type("{} as {}.{}".format(ob.__class__.__name__, role.__module__, role.__name__),
                 (role_base, ob.__class__),
                 members)

        i = object.__new__(c)
        if hasattr(ob, '__dict__'):
            super(role.__bases__[0], i).__setattr__('__dict__', ob.__dict__)
        return i

    def __init__(self, ob, ctx=None):
        pass

    __hash__ = _role_hash

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        return getattr(self.__ob__, attr)


class Role(RoleBase):
    def __delattr__(self, item):
        delattr(self.__ob__, item)

    def __setattr__(self, name, value):
        assert hasattr(self.__ob__,
                       name), "{} trying to set non-existing attribute of name '{}'.Roles should be stateless.".format(
            self.__class__.__name__, name)
        setattr(self.__ob__, name, value)


class StageProp(RoleBase):
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
            # #dict([(rn, rc) for rn, rc in roles if rn != n]))
            # wrapped = [rm[1] for rm in inspect.getmembers(r, inspect.ismethod) if hasattr(rm[1], 'wrapped')]
            setattr(c, n, RoleDescriptor(r))
        i = object.__new__(c)
        return i
