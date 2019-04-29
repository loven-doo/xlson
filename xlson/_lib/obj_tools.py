def expand_attrs_dict(attrs_dict, *keys):
    new_attrs_dict = attrs_dict.copy()
    for key in keys:
        try:
            new_attrs_dict[key] = attrs_dict[key].__dict__
        except AttributeError:
            pass
    return new_attrs_dict
