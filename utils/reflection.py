from importlib import import_module


def import_class(path: str):
    """Import a class from a full dotted path string."""
    module_name, class_name = path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, class_name)
