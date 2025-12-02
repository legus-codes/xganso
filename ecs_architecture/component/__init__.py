import importlib
import pkgutil

COMPONENTS = []


for _, module_name, ispkg in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
    if ispkg:
        continue

    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'test_config'):
            COMPONENTS.append(module)
    except:
        continue
