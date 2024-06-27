import fitz

from structures.graph.graph import Graph
from structures.trie.trie import Trie


class DocumentProcessor:
    def __init__(self):
        self.graph = Graph(True)
        self.trie = Trie()
        self.skip_pages = 0

    def get_proccessed_pdf(self, pdf_path, skip_pages=0):
        self.skip_pages = skip_pages

        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            if page_num < self.skip_pages:
                continue
            page = doc.load_page(page_num)

            self.page_proccessing(page, page_num - self.skip_pages + 1)
            self.word_proccessing(page, page_num - self.skip_pages + 1)

        return self.graph, self.trie

    def page_proccessing(self, page, page_num):
        text = page.get_text()
        vertex = None
        pageVertex = self.graph.get_vertex(page_num)
        if pageVertex:  ## if page added by reference
            pageVertex.set_element(
                {
                    "id": page_num,
                    "content": text,
                }
            )
            vertex = pageVertex
        else:
            pageVertexData = {
                "id": page_num,
                "content": text,
            }
            vertex = self.graph.insert_vertex(pageVertexData)

        self.add_page_references(vertex, page)

    def add_page_references(self, vertex, page):
        page_references = self.search_for_page_reference(
            page
        )  ## search for page references
        for ref in page_references:
            ref_vertex = self.graph.get_vertex(ref)
            if ref_vertex:  ### if page added by reference
                self.graph.insert_edge(vertex, ref_vertex)
            else:  ### if page not added by reference
                ref_page = {
                    "id": ref,
                    "content": "",
                }
                ref_vertex = self.graph.insert_vertex(ref_page)
                self.graph.insert_edge(vertex, ref_vertex)

    def word_proccessing(self, page, page_num):
        words = [word[4] for word in page.get_text("words")]
        for word in words:
            self.trie.insert(word, page_num)

    def search_for_page_reference(self, page):
        words = [word[4] for word in page.get_text("words")]
        page_refrences = []
        for index, word in enumerate(words):
            try:
                if "page" in word and (words[index + 1][0].isdigit()):
                    page_num = words[index + 1]
                    while not page_num.isdigit():
                        page_num = page_num[:-1]
                    page_refrences.append(int(page_num))
            except IndexError:
                pass
        return page_refrences
