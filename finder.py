class Finder:
    def __init__(self, graph, trie):
        self.graph = graph
        self.trie = trie

    def find(self, phrase):
        items = self.process_phrase(phrase)
        score = {}

        for index, item in enumerate(items):
            if index == 0:
                score = self.get_trie_score(item)
                graph_score = self.get_graph_score(score.keys())
                for key in score.keys():
                    score[key] += graph_score[key]

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

    def get_graph_score(self, score):
        pass

    def get_trie_score(self, word):
        pass
