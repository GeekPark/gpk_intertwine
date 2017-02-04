
def lazy_prop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazy_prop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_prop