from doc_processor import DocumentProcessor
from finder import Finder


def main():
    pdf_processor = DocumentProcessor()

    graph, trie = pdf_processor.get_proccessed_pdf(
        "literature/Data Structures and Algorithms in Python.pdf", 22
    )
    finder = Finder(graph, trie)

    while True:
        phrase = input("Please enter a phrase to search: ")
        if phrase == "exit":
            break
        finder.find(phrase)
        input()


if __name__ == "__main__":
    main()
