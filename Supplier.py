def duplicate(class_: type, args: dict, attributes: dict):  # Duplicate a class and preset attributes
    new = class_(**args)
    for attr, value in attributes.items():
        new.__setattr__(attr, value)
    return new
