def old_func(positional_arg, arg_with_default=None, *varargs, **kwargs):
    """Simple demonstration of old function signatures"""
    print('Required arg:    {}'.format(positional_arg))
    print('Optional arg:    {}'.format(arg_with_default))
    print('Unnamed varargs: {}'.format(varargs))
    print('Keyword varargs: {}'.format(kwargs))


old_func(1, 2, 3, 4, a=5, b=6)


# But what if we want this?
# make_list(*args, reverse=False)


def make_list(*args, **kwargs):
    """If we want to both capture positional varargs and have optional keyword
    args, we have to do this crap
    """
    bad_kwargs = set(kwargs.keys()) - {'reverse'}
    if bad_kwargs:
        fmt = ("varargs_and_optional_kwargs() got an unexpected keyword"
               " argument '{}'")
        raise TypeError(fmt.format(bad_kwargs.pop()))
    if kwargs.get('reverse', False):
        return list(reversed(args))
    else:
        return list(args)


print('Non-reversed: {}'.format(make_list(1, 2, 3)))
print('Reversed:     {}'.format(make_list(1, 2, 3, reverse=True)))
# fails:
# varargs_and_optional_kwargs(1, 2, 3, donut=True)


def make_list_3(*args, reverse=False):
    """Much better!"""
    if reverse:
        return list(reversed(args))
    else:
        return list(args)

print('Non-reversed: {}'.format(make_list_3(1, 2, 3)))
print('Reversed:     {}'.format(make_list_3(1, 2, 3, reverse=True)))


def all_kw_only(*, a=None, b):
    print(a, b)

all_kw_only(a=1, b=2)
