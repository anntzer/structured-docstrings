"""A more robust replacement for matplotlib.docstring.Substitution.
"""

from collections import MutableMapping
import inspect
import re
from string import Formatter
import textwrap


class Interpolator:
    def __init__(self):
        self._keys = {}

    def __setitem__(self, key, value):
        self._keys[key] = inspect.cleandoc(value)

    def update(self, *args, **kwargs):
        MutableMapping.update(self, *args, **kwargs)

    def interpolate_doc(self, func):
        if func.__doc__ is not None:
            func.__doc__ = _Formatter().format(func.__doc__, **self._keys)
        return func


class _Formatter(Formatter):
    def parse(self, format_string):
        for literal_text, field_name, format_spec, conversion \
                in super().parse(format_string):
            if format_spec:
                raise ValueError(
                    "This custom docstring formatter uses the format_spec "
                    "field to store indentation information")
            try:
                last_line, = re.finditer(r"(?m)^ *\Z", literal_text)
            except ValueError:
                raise ValueError(
                    "Interpolation fields can only be preceded by whitespace "
                    "(which determine the indentation of the interpolated "
                    "string) on their own line")
            indent = last_line.group()
            # Store indent information in the format_spec field.
            yield literal_text, field_name, indent, conversion

    @staticmethod
    def format_field(value, format_spec):
        # Indent all lines, except the first one (which reuses the indent of
        # the format string).
        return textwrap.indent(value, format_spec)[len(format_spec):]
