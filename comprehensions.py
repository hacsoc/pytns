"""Dict and set comprehensions examples for Python 2.7 through 3.2."""

# You used to only have these:
squared_evens = [x**2 for x in range(8) if x % 2 == 0]
print('squared evens: {0}'.format(squared_evens))

# to get a dict you would do this:
# (makes {0: ‘A’, 1: ‘B’, ...})
letter_for_int = dict((i, chr(65+i)) for i in range(10))

# to get a set you would do this:
s = set(i for i in range(10))

def invert(d):
    """Swap keys and values on d"""
    return {v: k for k, v in d.items()}

def even_keys(d):
    """Return a set of all even keys from d"""
    return {k for k in d.keys() if k % 2 == 0}

d = {i : chr(65+i) for i in range(10)}
print('dictionary:    {0}'.format(d))
print('inverted:      {0}'.format(invert(d)))
print('evens only:    {0}'.format(even_keys(d)))
print('set literal:   {0}'.format({0, 1, 2, 3, 4}))
