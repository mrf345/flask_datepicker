def find(function, items):
    '''Utility to find the first matching item in a list.

    Parameters
    ----------
    function : callable
        function that returns bool to check if the passed item matches.
    items : list
        list of items to search.
    '''
    for item in items:
        if function(item):
            return item
