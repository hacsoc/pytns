"""A simple demonstration of class decorators.

Consider this example:

    class Printer(object):
        def print(self, string:str) -> types.NoneType:
            pass

Printer.print() takes one string argument and returns None.

Now we implement it:

    @implements(Printer, check_method_arg_types=True)
    class StdoutPrinter(object):
        def print(self, string):
            print(string)

This will succeed:

    StdoutPrinter().print('hello')

This will fail with a TypeError:

    StdoutPrinter().print(1)

These classes will cause exceptions at import time:

    @implements(Printer, check_method_arg_types=True)
    class NonPrintingPrinter(object):
        def do_not_print(self, string):
            pass

    @implements(Printer, check_method_arg_types=True)
    class WrongArgsPrinter(object):
        def print(self, string, extra_arg):
            pass

    @implements(Printer, check_method_arg_types=True)
    class WrongReturnPrinter(object):
        def print(self, string):
            print(string)
            return 1
"""
import functools
import inspect
import types

spec_attrs_to_check = {'args', 'varargs', 'defaults', 'kwonlyargs'}

def _methods_in_a_not_b(a:type, b:type):
    """Return method names that are present in class B but not in class A"""
    a_keys = set(a.__dict__.keys())
    b_keys = set(b.__dict__.keys())
    return a_keys.difference(b_keys)

def _function_signatures_match(func1:types.FunctionType,
                               func2:types.FunctionType):
    """Return True if all args, kwargs, kw-only args, and defaults match"""
    spec1 = inspect.getfullargspec(func1)
    spec2 = inspect.getfullargspec(func2)
    return all(lambda: getattr(spec1, attr) != getattr(spec2, attr)
                       for attr in spec_attrs_to_check)

def _validate_interface(conform_to:type, cls:type):
    """Return True if cls has all methods of conform_to with the correct
    signature
    """
    missing_methods = _methods_in_a_not_b(conform_to, cls)
    if missing_methods:
        fmt = '{0.__name__} is missing methods {1} from {2.__name__}'
        raise TypeError(fmt.format(cls, missing_methods, conform_to))
    for name, func in conform_to.__dict__.items():
        if not name.startswith('_'):
            if not _function_signatures_match(func, getattr(cls, name)):
                fmt = ("{0.__name__} method '{1}' does not conform to"
                       "{2.__name__}. Arg spec should be {3}.")
                raise TypeError(fmt.format(cls, name, conform_to,
                                            inspect.getfullargspec(func)))

def _validate_args(func, *args, **kwargs):
    """Raise an exception if args and kwargs do not match the annotations on
    func
    """
    spec = inspect.getfullargspec(func)
    annotations = spec.annotations
    call_args = inspect.getcallargs(func, *args, **kwargs)
    for arg_name, arg_type in annotations.items():
        if arg_name != 'return' and not isinstance(call_args[arg_name], arg_type):
            fmt = "Argument {0}={1} is not of type {2.__name__}"
            raise TypeError(fmt.format(arg_name, call_args[arg_name], arg_type))

def _wrap_func(func, cls_meth):
    """Wrap a function in type checks for its interface's annotations"""
    @functools.wraps(cls_meth)
    def arg_checking_func(*args, **kwargs):
        _validate_args(func, *args, **kwargs)
        ret = cls_meth(*args, **kwargs)
        ret_type = inspect.getfullargspec(func).annotations['return']
        if not isinstance(ret, ret_type) and not implements(ret_type)(ret):
            fmt = "Return value must be of type {0.__name__}, not {1.__name__}"
            raise TypeError(fmt.format(ret_type, type(ret)))
        return ret
    return arg_checking_func

def _wrap_methods_with_type_check(conform_to, cls):
    """Wrap all methods on cls matching methods in conform_to with type
    checks
    """
    for name, func in conform_to.__dict__.items():
        if not name.startswith('_'):
            setattr(cls, name, _wrap_func(func, getattr(cls, name)))

def implements(conform_to, check_method_arg_types=False):
    """Class decorator to declare that a class implements all methods in
    another class which by convention is its interface and contains no
    implementation
    """
    def check_conformity(cls):
        _validate_interface(conform_to, cls)
        if check_method_arg_types:
            _wrap_methods_with_type_check(conform_to, cls)
        return cls
    return check_conformity
