def expand_attrs_dict(attrs_dict, *keys):
    new_attrs_dict = attrs_dict.copy()
    for key in keys:
        try:
            new_attrs_dict[key] = attrs_dict[key].__dict__
        except AttributeError:
            pass
    return new_attrs_dict


def deepupdate_attrs(obj, attr_dict):
    for attr in obj.__dict__:
        try:
            obj = deepupdate_attrs(obj.__dict__[attr], attr_dict[attr])
        except AttributeError:
            obj.__dict__[attr] = attr_dict[attr]
    return obj
