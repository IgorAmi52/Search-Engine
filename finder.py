from pick import pick


class Finder:
    def __init__(self, graph, trie):
        self.graph = graph
        self.trie = trie

    def find(self, phrase):
        items = self.process_phrase(phrase)
        important_words = []
        score = {}

        i = 0
        operation = None
        while i < len(items):
            if items[i] == "&":  ### intersection
                operation = "&"

            elif items[i] == "|":  ### union
                operation = "|"

            elif items[i] == "!":  ### complement
                operation = "!"

            else:  ### word
                try:
                    trie_score = self.get_trie_score(items[i])
                    important_words.append(items[i])
                except ValueError as e:  ### if word not found
                    print(e)
                    pot_word = self.trie.find_potential_word(items[i])
                    option, _ = pick(["Yes", "No"], "Did you mean: " + pot_word + "?")
                    if option == "Yes":
                        items[i] = pot_word
                        continue
                    return None, None
                if operation is None:
                    score = trie_score  ### first score
                elif operation == "&":
                    score = self.get_intersection_score_dict(score, trie_score)
                    important_words.append(items[i])
                elif operation == "|":
                    score = self.get_union_score_dict(score, trie_score)
                    important_words.append(items[i])
                elif operation == "!":
                    score = self.get_complement_score_dict(score, trie_score)
                operation = None
                graph_score = self.get_graph_score(score.keys())
                for key in score.keys():
                    score[key] += graph_score[key]
            i += 1
        return score, important_words

    def process_phrase(self, phrase):
        raw_words = phrase.split()

        for index, word in enumerate(raw_words):
            word = word.lower()
            if word == "and":
                raw_words[index] = "&"
            elif word == "or":
                raw_words[index] = "|"
            elif word == "not":
                raw_words[index] = "!"
            else:
                raw_words[index] = self.keep_only_alpha(word)
        return raw_words

    def keep_only_alpha(self, word):
        return "".join([char for char in word if char.isalpha()])

    def get_intersection_score_dict(self, dict1, dict2):
        pop_keys = []
        for key in dict1.keys():
            if key in dict2:
                dict1[key] += dict2[key]
            else:
                pop_keys.append(key)
        for key in pop_keys:
            dict1.pop(key)
        return dict1

    def get_union_score_dict(self, dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] += dict2[key]
            else:
                dict1[key] = dict2[key]
        return dict1

    def get_complement_score_dict(self, dict1, dict2):
        pop_keys = []
        for key in dict2.keys():
            if key in dict1:
                dict1.pop(key)
        for key in pop_keys:
            dict1.pop(key)
        return dict1

    def get_graph_score(self, keys):
        graph_score = {}
        for key in keys:
            graph_score[key] = 0
            if key in self.graph._outgoing:
                graph_score[key] = -len(self.graph._outgoing[key])
            if key in self.graph._incoming:
                graph_score[key] = +len(self.graph._incoming[key]) * 2
        return graph_score

    def get_trie_score(self, word):
        ret = self.trie.search(word)
        if ret == {}:
            raise ValueError(word + " not found in the document.")
        return ret
