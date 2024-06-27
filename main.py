import os
import dill
import pick
from services.doc_processor import DocumentProcessor
from services.finder import Finder
from services.printer import Printer
from services.writer import Writer


def main():
    try:
        with open("parsed_data/graph.dill", "rb") as dill_file:
            graph = dill.load(dill_file)
        with open("parsed_data/trie.dill", "rb") as dill_file:
            trie = dill.load(dill_file)
    except FileNotFoundError:
        pdf_processor = DocumentProcessor()

        graph, trie = pdf_processor.get_proccessed_pdf(
            "data/Data Structures and Algorithms in Python.pdf", 22
        )
        with open("parsed_data/graph.dill", "wb") as json_file:
            dill.dump(graph, json_file)
        with open("parsed_data/trie.dill", "wb") as json_file:
            dill.dump(trie, json_file)

    finder = Finder(graph, trie)
    printer = Printer(graph)
    writer = Writer(graph)

    while True:
        os.system("clear")
        phrase = input("Please enter a phrase to search or exit to exit: ")
        if phrase == "exit":  ### exit the program
            break
        if phrase[-1] == "*":  ### if the phrase ends with * then find suggestions
            suggestions = trie.find_suggestions(phrase[:-1])
            printer.print_suggestions(suggestions)
            continue

        score, important_words = finder.find(phrase)

        sorted_keys = printer.print_best_results(score, important_words)
        if sorted_keys is not None:
            option, _ = pick.pick(["Yes", "No"], "Do you want to save the results?")
            if option == "Yes":
                writer.narrow_and_create_pdf(sorted_keys, important_words)


if __name__ == "__main__":
    main()
