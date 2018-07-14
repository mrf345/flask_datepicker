from inspect import (
    getargspec, getsourcefile, isclass, signature
)

def function_parameters(function):
    """
    Simple decorator to raise a TypeError, if paramater
    and it's static type added to the description __doc__
    as such (parameter_name: str)
    """
    if not callable(function):
        raise TypeError(
            'function_parameters(function=%s) you must pass a function' % (
                function
            )
        )
    def wrapper(*args, **kwargs):
        if function.__doc__ is not None:
            if len(function.__doc__) > 3 and len(
                    args) + len(kwargs) + len(function.__defaults__ if function.__defaults__ else '') >= len(
                        list(signature(function).parameters)):
                paras_index = [
                    p for p in list(signature(
                        function
                    ).parameters) if p not in kwargs.keys()
                ]
                for content in [i.split('))')[0
                ] for i in function.__doc__.replace(
                    ' ', '').split('((') if ':' in i and i.split(
                        ':')[0] in paras_index or i.split(':'
                        )[0] in kwargs.keys()]:
                    con = content.split(':')
                    try:
                        if not isinstance(eval(con[1]), type):
                            raise TypeError()
                    except Exception:
                        raise TypeError(
                            "function_parameters(%s(%s=%s)) " % (
                                getsourcefile(function) + 
                                ' ' + function.__name__,
                                con[0], con[1]
                            ) + "wrong type given in __doc__" 
                        )
                    received_arg = kwargs.get(
                        con[0]) if kwargs.get(
                                con[0]
                                ) else args[
                                    paras_index.index(
                                        con[0])]
                    if type(received_arg) != eval(con[1]):
                        raise TypeError(
                            "%s(%s=%s) requires type %s" % (
                                getsourcefile(function) + 
                                ' ' + function.__name__,
                                con[0], type(received_arg),
                                eval(con[1])
                            )
                        )
        return function(*args, **kwargs)
    return wrapper

def class_parameters(decorator):
    """
    To wrap all class methods with static_parameters decorator 
    """
    def decorate(the_class):
        if not isclass(the_class):
            raise TypeError(
                'class_parameters(the_class=%s) you must pass a class' % (
                    the_class
                )
            )
        for attr in the_class.__dict__:
            if callable(
                getattr(
                    the_class, attr)):
                setattr(
                    the_class, 
                    attr, 
                    decorator(
                        getattr(the_class, attr)))
        return the_class
    return decorate

