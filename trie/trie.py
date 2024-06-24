class TrieNode:
    def __init__(self):
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
