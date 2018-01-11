"""A more robust replacement for matplotlib.docstring.Substitution.
"""

import inspect
import re
from string import Formatter
import sys
import pydoc
import textwrap


def interpolate_doc(func):
    if func.__doc__ is not None:
        func.__doc__ = _Formatter().format(
            func.__doc__, **sys._getframe(1).f_globals)
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
    def get_field(field_name, args, kwargs):
        try:
            return Formatter().get_field(field_name, args, kwargs)
        except KeyError:
            return pydoc.locate(field_name), None

    @staticmethod
    def format_field(value, format_spec):
        # Indent all lines, except the first one (which reuses the indent of
        # the format string).
        return textwrap.indent(inspect.cleandoc(value),
                               format_spec)[len(format_spec):]
