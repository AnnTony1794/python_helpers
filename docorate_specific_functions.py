import re 


def decorate_specific_methods(decorator, methods_starting_with: str):
    """
    Decorator that decorates all the methods, of a class,
    whose name begins with 'methods_starting_with' with your own decorator 'my_decorator'.
    arguments:
        method_starting_with: str
        decorator: function that receives another function as a parameter
                   and its wrapper function receives 'self'

    Ex:
        def my_decorator(method):
            def wrapper(self, *args, **kwargs):
                # Extra code
                method(self, *args, **kwargs)
                # Extra code
            return wrapper

    Make sure to add the *args and **kwargs so you can use whatever number of arguments you need
	
	Usage:
	
		@decorate_specific_methods(my_decorator, methods_starting_with="_ex")
		class Fizz:
			def _ex_func_1(self):
				pass
			def _ex_func_2(self, var):
				return var
    """
    def get_current_class_methods(cls):
        """Remove parent and magic methods"""
        methods = set(dir(cls)) - {method for parent in cls.__bases__ for method in dir(parent)}
        return list(filter(
            lambda x: x.startswith(methods_starting_with) and not re.match(r'_.*_', x), methods))

    def decorate(cls):
        assert inspect.isclass(cls), "This decorator only works on classes"
        methods = get_current_class_methods(cls)
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls
    return decorate
