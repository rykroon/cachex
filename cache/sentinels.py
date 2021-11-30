

Undefined = object()


class NotPassed:
    ...


class NotFound:
    ...


"""
    To Do:
        - Create sentinel value NotPassed for differentiating between None and a kwarg that was not passed.
        - Create sentinel value NotFound for differentiating between None and a key not being found in the cache.
"""