import inspect

def check(given: object, expected: type, valueName, catch=False):
    if not isinstance(given, expected):
        if not catch:
            raise TypeError(f"Value {valueName}. Expected: {expected}, Given: {given}")
        return 0
    return 1

def require(**expected_types):
    def decorator(func):
        if any(not isinstance(t, type) for t in expected_types.values()):
            raise TypeError("Each type should be \"type\" objects.")
        sig = inspect.signature(func)
        param_names = list(sig.parameters)

        def wrapper(*args, **kwargs):
            combined_args = dict(zip(param_names, args))
            combined_args.update(kwargs)
            for arg_name, expected_type in expected_types.items():
                if arg_name in combined_args:
                    value = combined_args[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(f"Argument '{arg_name}' should be a {expected_type.__name__} object, "
                                        f"given: {type(value).__name__}")
            return func(*args, **kwargs)

        return wrapper
    return decorator
