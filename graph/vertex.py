class Vertex:
    """Struktura koja predstavlja čvor grafa."""

    __slots__ = "_element"

    def __init__(self, x):
        self._element = x

    def element(self):
        """Vraća element vezan za čvor grafa."""
        return self._element

    def __hash__(self):  # omogućava da Vertex bude ključ mape
        return hash(id(self))

    def __str__(self):
        return str(self._element)
