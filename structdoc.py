from collections import OrderedDict
import inspect


class ParsedDocstring(str):
    def __new__(cls, s, kwargs):
        self = super().__new__(cls, s)
        kwargs["parameters"] = OrderedDict(kwargs.get("parameters", []))
        self._kwargs = kwargs
        return self

    summary = property(lambda self: self._kwargs["summary"])
    parameters = property(lambda self: self._kwargs["parameters"])


class LazyDocstring(ParsedDocstring):
    def __new__(cls, s, kwargs, func):
        # *s* is unused but kept to maintain a signature similar to the parent
        # class.
        self = super().__new__(cls, s, kwargs)
        self._func = func
        return self

    def _render(self):
        parts = []
        if self.summary is not None:
            parts.append(inspect.cleandoc(self.summary))
        if self.parameters is not None:
            parts.append(inspect.cleandoc("""
                Parameters
                ----------"""))
            for v in self.parameters.values():
                parts.append(inspect.cleandoc(v))
        doc = "\n\n".join(parts)
        self._func.__doc__ = ParsedDocstring(doc, self._kwargs)
        return doc

    locals().update(
        {_name: property(lambda self, _name=_name:
                         getattr(self._render(), _name))
         for _name in
         set(vars(str)) - {"__doc__", "__getattribute__", "__new__"}})


def process_docstring(**kwargs):
    def decorator(func):
        if func.__doc__ is not None:
            raise ValueError("A docstring already exists!")
        func.__doc__ = LazyDocstring("", kwargs, func)
        return func
    return decorator
