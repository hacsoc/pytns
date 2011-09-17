"""Function annotation example for Python 3.0 and later."""

# http://www.python.org/dev/peps/pep-3107/

import inspect

def cat(a:str, b:str) -> str:
    return a + b

spec = inspect.getfullargspec(cat)
print(spec.annotations)

print(cat(1, 2))
