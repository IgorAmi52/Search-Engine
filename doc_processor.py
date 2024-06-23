import fitz

from graph.graph import Graph
from trie.trie import Trie


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
            self.page_proccessing(page.get_text(), page_num - self.skip_pages + 1)
            self.word_proccessing(page.get_text(), page_num - self.skip_pages + 1)

        return self.graph, self.trie

    def page_proccessing(self, text, page_num):
        page = self.graph.get_vertex(page_num)
        if page:  ## if page added by reference
            page.set_element(
                {
                    "id": page_num,
                    "content": text,
                    "paragraphs": self.split_text_into_paragraphs(text),
                }
            )
        else:
            page = {
                "id": page_num,
                "content": text,
                "paragraphs": self.split_text_into_paragraphs(text),
            }
            vertex = self.graph.insert_vertex(page)

        page_references = self.search_for_page_reference(
            text
        )  ## search for page references
        for ref in page_references:
            print(ref)
            ref_vertex = self.graph.get_vertex(ref)
            if ref_vertex:  ### if page added by reference
                self.graph.insert_edge(vertex, ref_vertex)
            else:  ### if page not added by reference
                ref_page = {
                    "id": ref,
                    "content": "",
                    "paragraphs": [],
                }
                ref_vertex = self.graph.insert_vertex(ref_page)
                self.graph.insert_edge(vertex, ref_vertex)

    def word_proccessing(self, text, page_num):
        words = text.split()
        for word in words:
            self.trie.insert(word, page_num)

    def split_text_into_paragraphs(self, text):
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs

    def search_for_page_reference(self, text):
        words = text.split()
        page_refrences = []
        for index, word in enumerate(words):
            if "page" in word and (words[index + 1][0].isdigit()):
                page_num = words[index + 1]
                while not page_num.isdigit():
                    page_num = page_num[:-1]
                page_refrences.append(int(page_num))
        return page_refrences
