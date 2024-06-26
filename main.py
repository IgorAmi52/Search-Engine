import os
import dill
from doc_processor import DocumentProcessor
from finder import Finder
from printer import Printer


def main():
    pdf_processor = DocumentProcessor()

    try:
        with open("parsed_data/graph.dill", "rb") as json_file:
            graph = dill.load(json_file)
        with open("parsed_data/trie.dill", "rb") as json_file:
            trie = dill.load(json_file)
    except FileNotFoundError:
        graph, trie = pdf_processor.get_proccessed_pdf(
            "data/Data Structures and Algorithms in Python.pdf", 22
        )
        with open("parsed_data/graph.dill", "wb") as json_file:
            dill.dump(graph, json_file)
        with open("parsed_data/trie.dill", "wb") as json_file:
            dill.dump(trie, json_file)

    finder = Finder(graph, trie)
    printer = Printer(graph)

    while True:
        os.system("clear")
        phrase = input("Please enter a phrase to search or exit to exit: ")
        if phrase == "exit":
            break
        if phrase[-1] == "*":
            suggestions = trie.find_suggestions(phrase[:-1])
            printer.print_suggestions(suggestions)
            continue
        score, important_words = finder.find(phrase)
        if score is not None:
            printer.print_best_results(score, important_words)


if __name__ == "__main__":
    main()
