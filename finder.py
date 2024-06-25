class Finder:
    def __init__(self, graph, trie):
        self.graph = graph
        self.trie = trie

    def find(self, phrase):
        items = self.process_phrase(phrase)
        score = {}

        i = 0
        operation = None
        while i < len(items):
            if items[i] == "&":  ### intersection
                operation = "&"
                continue
            elif items[i] == "|":  ### union
                operation = "|"
                continue
            elif items[i] == "!":  ### complement
                operation = "!"
                continue
            else:  ### word
                if operation is None:
                    score = self.get_trie_score(items[i])  ### first score
                elif operation == "&":
                    score = self.get_intersection_score_dict(
                        score, self.get_trie_score(items[i])
                    )
                elif operation == "|":
                    score = self.get_union_score_dict(
                        score, self.get_trie_score(items[i])
                    )
                elif operation == "!":
                    score = self.get_complement_score_dict(
                        score, self.get_trie_score(items[i])
                    )
            graph_score = self.get_graph_score(score.keys())
            for key in score.keys():
                score[key] += graph_score[key]
            i += 1

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
        for key in dict1.keys():
            if key in dict2:
                dict1[key] += dict2[key]
            else:
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
        for key in dict2.keys():
            if key in dict1:
                dict1.pop(key)
        return dict1

    def get_graph_score(self, score):
        pass

    def get_trie_score(self, word):
        ret = self.trie.search(word)
        if ret == {}:
            raise ValueError("Word not found in the document.")
