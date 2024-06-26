import random


class TrieNode:
    def __init__(self):
        self.parent = None
        self.children = {}
        self.is_end_of_word = False
        self.document_ids = {}


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, doc_id):
        node = self.root
        for char in word:
            if not char.isalpha():
                continue
            char = char.lower()
            if char not in node.children:
                node.children[char] = TrieNode()
            node.children[char].parent = node
            node = node.children[char]
        node.is_end_of_word = True
        if doc_id not in node.document_ids:
            node.document_ids[doc_id] = 1
        else:
            node.document_ids[doc_id] += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return {}
            node = node.children[char]
        return node.document_ids if node.is_end_of_word else {}

    def find_potential_word(self, word):
        node = self.root
        pot_word = ""
        for char in word:  ### find the longest prefix of the word that is in the trie
            if char not in node.children:
                break
            pot_word += char
            node = node.children[char]

        while len(node.children) != 0:  ### find the word that is in the trie
            next_char = random.choice(list(node.children.keys()))
            node = node.children[next_char]
            pot_word += next_char
        return pot_word

    def find_suggestions(self, word, node=None, suggestions=[]):
        if node is None:  ### if the function is called for the first time
            node = self.root
            for char in word:
                if char not in node.children:
                    return {}
                node = node.children[char]

        for char in node.children:
            word += char
            self.find_suggestions(word, node.children[char], suggestions)
            word = word[:-1]
        if node.is_end_of_word:
            suggestions.append(word)
        return suggestions
