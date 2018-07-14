from static_parameters import function_parameters

def a(a, b):
    """((a:str)) ((b:int))"""
    return a * b


def all_functions(globe=globals()):
    for function in {k:v for k,v in globe.items() if v}:
        if callable(globe.get(function)):
            globe[function] = function_parameters(
                globe.get(function)
            )
