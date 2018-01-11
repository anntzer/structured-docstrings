from interpolate import interpolate_doc


foo = """
    hello
    world
"""
bar = "foo bar\nbaz"


@interpolate_doc
def func():
    """
    this is a docstring

    {interpolate_example.foo}

        {bar}
    """


try:
    @interpolate_doc
    def bad_doc():
        """
        fields {must} be preceded by whitespace
        """
except ValueError:
    print("error correctly caught")
