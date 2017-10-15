from structdoc import process_docstring


@process_docstring(
    summary="""
    Some great docstring.
    """,
    parameters=[
        ("foo", """
         foo : int
             The description of foo.
         """),
        ("bar", """
         bar : str
             The description of bar.
         """),
    ],
)
def func(foo, bar):
    pass


@process_docstring(
    summary="""
    Some other docstring.
    """,
    parameters=[
        ("foo", func.__doc__.parameters["foo"]),
    ],
)
def otherfunc(foo):
    pass
