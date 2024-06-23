from graph.vertex import Vertex
from graph.edge import Edge


class Graph:
    def __init__(self, directed=False):
        """Kreira prazan graf (podrazumevana vrednost je da je neusmeren).

        Ukoliko se opcioni parametar directed postavi na True, kreira se usmereni graf.
        """
        self._outgoing = {}
        # ukoliko je graf usmeren, kreira se pomoćna mapa
        self._incoming = {} if directed else self._outgoing

    def _validate_vertex(self, v):
        """Proverava da li je v čvor(Vertex) ovog grafa."""
        if not isinstance(v, Vertex):
            raise TypeError("Očekivan je objekat klase Vertex")
        if v not in self._outgoing:
            raise ValueError("Vertex ne pripada ovom grafu.")

    def is_directed(self):
        """Vraća True ako je graf usmeren; False ako je neusmeren."""
        return (
            self._incoming is not self._outgoing
        )  # graf je usmeren ako se mape razlikuju

    def vertex_count(self):
        """Vraća broj čvorova u grafu."""
        return len(self._outgoing)

    def vertices(self):
        """Vraća iterator nad svim čvorovima grafa."""
        return self._outgoing.keys()

    def edge_count(self):
        """Vraća broj ivica u grafu."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # ukoliko je graf neusmeren, vodimo računa da ne brojimo čvorove više puta
        return total if self.is_directed() else total // 2

    def edges(self):
        """Vraća set svih ivica u grafu."""
        result = (
            set()
        )  # pomoću seta osiguravamo da čvorove neusmerenog grafa brojimo samo jednom
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())  # dodavanje ivice u rezultujući set
        return result

    def get_edge(self, u, v):
        """Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Vraća sve (odlazne) ivice iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def get_vertex(self, vertex_id):
        for vertex in self.vertices():
            if vertex.get_id() == vertex_id:
                return vertex
        return None

    def insert_vertex(self, x=None):
        """Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
        v = Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # mapa različitih vrednosti za dolazne čvorove
        return v

    def insert_edge(self, u, v, x=None):
        """Ubacuje i vraća novu ivicu (Edge) od u do v sa pomoćnim elementom x.

        Baca ValueError ako u i v nisu čvorovi grafa.
        Baca ValueError ako su u i v već povezani.
        """
        if self.get_edge(u, v) is None:  # uključuje i proveru greške
            e = Edge(u, v, x)
            self._outgoing[u][v] = e
            self._incoming[v][u] = e
