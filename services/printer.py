import os
import re


class Printer:
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, graph):
        self._graph = graph

    def print_best_results(self, score, words):
        sorted_keys = self.get_sorted_keys(score)
        if len(sorted_keys) == 0:
            input("No results found! \n")
            return None
        i = 0
        while True:
            for j in range(5):
                if i + j < len(sorted_keys):
                    print("\nResult ", i + j + 1, " of ", len(sorted_keys))
                    self._print_result(sorted_keys[i + j], words)
            i += 5
            if i >= len(sorted_keys):
                input("\nPress Enter to continue: ")
                break
            option = input(
                "\nType next to write next 5 results or type whatever to exit: "
            )
            if option != "next":
                break
            os.system("clear")

        return sorted_keys

    def _print_result(self, key, words):
        page = self._graph.get_vertex(key).get_element()
        rows = page.split("\n")
        imporant_rows = []

        print("Page: ", str(key) + "\n")
        for row in rows:
            row_low = row.lower()
            if any(word in row_low for word in words):
                for word in words:
                    row = re.sub(
                        word,
                        self.RED + word.upper() + self.RESET,
                        row,
                        flags=re.IGNORECASE,
                    )
                imporant_rows.append(row)
        for row in imporant_rows:
            print("..." + row + "...")

    def get_sorted_keys(self, score):
        ret = []
        for key in score.keys():
            if score[key] > 0:
                ret.append(key)
        return sorted(ret, key=lambda x: score[x], reverse=True)

    def print_suggestions(self, suggestions):
        if not suggestions:
            input("No suggestions found.")
            return
        print("Autocomplete suggestions: \n")
        for index, suggestion in enumerate(suggestions):
            print(suggestion, end=", " if index < len(suggestions) - 1 else " ")
        input("\nPress Enter to continue: ")
