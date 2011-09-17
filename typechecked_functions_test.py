from typechecked_functions import typecheck


def assert_raises(exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        assert False
    except exception:
        assert True


def assert_doesnt_raise(exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exception:
        assert False


def test_functions():

    @typecheck
    def print_integer(i:int) -> type(None):
        print(i)

    assert_doesnt_raise(TypeError, print_integer, 1)
    assert_raises(TypeError, print_integer, 'not an integer')


def test_classes():

    @typecheck
    class TypecheckedClass(object):

        def print_integer(self, i:int) -> type(None):
            print(i)

        def print_anything(self, anything):
            print(anything)

    obj = TypecheckedClass()
    assert_doesnt_raise(TypeError, obj.print_integer, 1)
    assert_raises(TypeError, obj.print_integer, 'not an integer')
    assert_doesnt_raise(TypeError, obj.print_anything, 'anything')
