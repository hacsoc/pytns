"""String formatting examples for Python 2.6 through 3.2."""

a = 'Tom'
b = 'Dick'
d = 'Harry'

# old:
print("The story of %s, %s, and %s" % (a, b, d))
print("The story of %(a)s, %(b)s, and %(d)s" % locals())

# new:
# http://www.python.org/dev/peps/pep-3101/
print("The story of {0}, {1}, and {c}".format(a, b, c=d))
print("The story of {a}, {b}, and {d}".format(**locals()))

some_dict = dict(a=1, b=2)
some_dict2 = {'a': 1, 'b': 2}
assert some_dict == some_dict2

print("Item 'a' in {0.__class__.__name__}: {0[a]}".format(some_dict))
