import pkgutil
import inspect
from proxypool.crawler.base import Base
from proxypool.crawler.proxysite import crawlerPath

classes = []
for loader, name, is_pkg in pkgutil.walk_packages([crawlerPath]):
    # get module type
    module = loader.find_module(name).load_module(name)
    for _class, _class_object in inspect.getmembers(module, callable):
        # filter class object
        if inspect.isclass(_class_object) and issubclass(_class_object, Base) \
                and _class_object is not Base and _class_object.isvalid:
            classes.append(_class_object)

__all__ = ['classes']
