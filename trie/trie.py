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
        word_shallow = True
        for char in word:  ### find the longest prefix of the word that is in the trie
            if char not in node.children:
                word_shallow = False
                break
            node = node.children[char]
        if not word_shallow:  ### if the word is not in the trie, find the longest prefix that is in the trie
            while not node.is_end_of_word and node.children:
                node = node.parent
                word = word[:-1]
        while not node.is_end_of_word:  ### find the word that is in the trie
            next_char = list(node.children.keys())[0]
            node = node.children[next_char]
            word += next_char
        return word
