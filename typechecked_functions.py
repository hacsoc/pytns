"""Demonstration of how function annotations might be useful to check the types
of input and output values on an arbitrary function. Python 3.0 and later.
"""

import functools
import inspect
import types


def _typechecked_func(func):
    """Return a function wrapped in typechecks"""

    # Preserve the function signature
    @functools.wraps(func)
    def arg_checking_func(*args, **kwargs):

        # Get the annotation dict from the arg spec
        spec = inspect.getfullargspec(func)
        annotations = spec.annotations

        # Get the dict of {arg name: arg value}
        call_args = inspect.getcallargs(func, *args, **kwargs)

        # Check each argument for type if the annotation contains it
        for arg_name, arg_type in annotations.items():
            if (arg_name != 'return'
               and not isinstance(call_args[arg_name], arg_type):
                fmt = "Argument {0}={1} is not of type {2.__name__}"
                raise TypeError(fmt.format(arg_name,
                                           call_args[arg_name], arg_type))

        # Check the return value as well if necessary
        ret = func(*args, **kwargs)
        if 'return' in annotations:
            ret_type = annotations['return']
            if not isinstance(ret, ret_type):
                fmt = ("Return value must be of type {0.__name__},"
                       " not {1.__name__}")
                raise TypeError(fmt.format(ret_type, type(ret)))

        return ret

    return arg_checking_func


def _typechecked_class(cls):
    """Replace all non-builtin methods with typechecked versions"""
    for name, func in cls.__dict__.items():
        if not name.startswith('__'):
            setattr(cls, name, _typechecked_func(func))
    return cls


def typecheck(item):
    """Add type checks to a function or class based on the annotations"""
    if isinstance(item, types.FunctionType):
        return _typechecked_func(item)
    elif isinstance(item, type):
        return _typechecked_class(item)
    else:
        raise TypeError('Can only typecheck classes and functions')
