def find(validator, items):
    '''Utility to find the first matching item in a list.

    Parameters
    ----------
    validator : callable
        function that returns bool to check if the passed item matches.
    items : list
        list of items to search.
    '''
    for item in items:
        if validator(item):
            return item


def cache_output(function):
    '''Helper decorator to cache a function output.

    Parameters
    ----------
    function : callable
        function to cache its output.

    Returns
    -------
    callable
        decorated function.
    '''
    def decorator(*args, **kwargs):
        key = '{}{}'.format(args, kwargs)
        output = function.__dict__.get(key, None)

        if not output:
            output = function.__dict__[key] = function(*args, **kwargs)

        return output
    return decorator
