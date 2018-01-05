from interpolate import Interpolator


interpd = Interpolator()
interpd.update(
    foo="""
        hello
        world
        """,
    bar="foo bar\nbaz")


@interpd.interpolate_doc
def func():
    """
    this is a docstring

    {foo}

        {bar}
    """


try:
    @interpd.interpolate_doc
    def bad_doc():
        """
        fields {must} be preceded by whitespace
        """
except ValueError:
    print("error correctly caught")
