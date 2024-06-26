class Vertex:
    """Struktura koja predstavlja čvor grafa."""

    __slots__ = "_element", "_id"

    def __init__(self, x):
        self._element = x

    def element(self):
        """Vraća element vezan za čvor grafa."""
        return self._element

    def set_element(self, x):
        self._element = x

    def get_element(self):
        return self._element["content"]

    def get_id(self):
        return self._element["id"]

    def __hash__(self):  # omogućava da Vertex bude ključ mape
        return self._element["id"]

    def __str__(self):
        return str(self._element)
