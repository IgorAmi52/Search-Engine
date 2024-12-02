import fitz


class Writer:
    def __init__(self, graph):
        self._graph = graph

    def narrow_and_create_pdf(
        self,
        page_keys,
        highlight_words,
        input_pdf="data/Data Structures and Algorithms in Python.pdf",
        output_pdf="output/output.pdf",
        skip_pages=22,
    ):
        pdf_document = fitz.open(input_pdf)
        new_pdf_document = fitz.open()

        # Iterate over the list of pages to extract
        for page_number in page_keys:
            new_pdf_document.insert_pdf(
                pdf_document,
                from_page=page_number + skip_pages - 1,
                to_page=page_number + skip_pages - 1,
            )
        for page_number in range(len(page_keys)):
            page = new_pdf_document.load_page(page_number)
            for word in highlight_words:
                text_instances = page.search_for(word)
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.update()

        # Save the new PDF document
        new_pdf_document.save(output_pdf)
        new_pdf_document.close()
        pdf_document.close()
