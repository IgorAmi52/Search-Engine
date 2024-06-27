from pick import pick


class Finder:
    def __init__(self, graph, trie):
        self.graph = graph
        self.trie = trie

    def find(self, phrase):
        items = self.process_phrase(phrase)
        score, important_words, brackets_score, _ = self.find_recursive(items, 0, [])
        if brackets_score != 0:
            print("Brackets are not balanced.")
            return None, None
        return score, important_words

    def find_recursive(self, items, brackets_score, important_words, i=0):
        score = {}
        operation = None
        while i < len(items):
            if items[i] == "&":  ### intersection
                operation = "&"
                i += 1
                continue
            elif items[i] == "|":  ### union
                operation = "|"
                i += 1
                continue
            elif items[i] == "!":  ### complement
                operation = "!"
                i += 1
                continue
            elif items[i] == "(":
                temp_score, important_words, brackets_score, index = (
                    self.find_recursive(
                        items[i + 1 :],
                        brackets_score + 1,
                        important_words,
                    )
                )
                i += index
            elif items[i] == ")":
                return score, important_words, brackets_score - 1, i + 1
            else:
                try:
                    temp_score = self.get_trie_score(items[i])
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
                score = self.add_graph_score(temp_score)
                ### first score
            elif operation == "&":
                score = self.get_intersection_score_dict(score, temp_score)
            elif operation == "|":
                score = self.get_union_score_dict(score, temp_score)
            elif operation == "!":
                score = self.get_complement_score_dict(score, temp_score)
            operation = None
            i += 1
        return score, important_words, brackets_score, None

    def process_phrase(self, phrase):
        raw_words = phrase.split()
        ret = []
        for word in raw_words:
            word = word.lower()
            if word[0] == "(":
                ret.append("(")
            elif word[-1] == ")":
                ret.append(word[:-1])
                ret.append(")")
                continue
            elif word == "and":
                ret.append("&")
                continue
            elif word == "or":
                ret.append("|")
                continue
            elif word == "not":
                ret.append("!")
                continue
            ret.append(self.keep_only_alpha(word))
        return ret

    def keep_only_alpha(self, word):
        return "".join([char for char in word if char.isalpha()])

    def add_graph_score(self, score):
        graph_score = self.get_graph_score(score.keys())
        for key in score.keys():
            score[key] += graph_score[key]
        return score

    def get_intersection_score_dict(self, dict1, dict2):
        pop_keys = []
        for key in dict1.keys():
            if key in dict2:
                dict1[key] += dict2[key]
            else:
                pop_keys.append(key)
        for key in pop_keys:
            dict1.pop(key)
        self.add_graph_score(dict1)
        return dict1

    def get_union_score_dict(self, dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] += dict2[key]
            else:
                dict1[key] = dict2[key]
        self.add_graph_score(dict1)
        return dict1

    def get_complement_score_dict(self, dict1, dict2):
        pop_keys = []
        for key in dict2.keys():
            if key in dict1:
                pop_keys.append(key)
        for key in pop_keys:
            dict1.pop(key)
        self.add_graph_score(dict1)
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
