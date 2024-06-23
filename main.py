from doc_processor import DocumentProcessor


def main():
    pdf_processor = DocumentProcessor()
    graph, trie = pdf_processor.get_proccessed_pdf(
        "literature/Data Structures and Algorithms in Python.pdf", 22
    )


if __name__ == "__main__":
    main()
