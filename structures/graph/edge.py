from graph.vertex import Vertex


class Edge:
    """Struktura koja predstavlja ivicu grafa"""

    __slots__ = "_origin", "_destination", "_element"

    def __init__(self, origin, destination, element):
        self._origin = origin
        self._destination = destination
        self._element = element

    def endpoints(self):
        """Vraća torku (u,v) za čvorove u i v."""
        return self._origin, self._destination

    def opposite(self, v):
        """Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
        if not isinstance(v, Vertex):
            raise TypeError("v mora biti instanca klase Vertex")
        if self._destination == v:
            return self._origin
        elif self._origin == v:
            return self._destination
        raise ValueError("v nije čvor ivice")

    def element(self):
        """Vraća element vezan za ivicu"""
        return self._element

    def __hash__(self):  # omogućava da Edge bude ključ mape
        return hash((self._origin, self._destination))

    def __str__(self):
        return "({0},{1},{2})".format(self._origin, self._destination, self._element)
