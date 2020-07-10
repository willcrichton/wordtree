from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from graphviz import Digraph


class Direction(Enum):
    Forward = 1
    Backward = 2


@dataclass
class FreqNode:
    freq: int
    children: Dict[str, "FreqNode"]


def build_tree(ngrams, frequencies):
    tree = FreqNode(freq=0, children={})
    for ngram, freq in zip(ngrams, frequencies):
        subtree = tree
        for gram in ngram:
            if gram not in subtree.children:
                subtree.children[gram] = FreqNode(children={}, freq=0)
            subtree = subtree.children[gram]
        subtree.freq = freq
    return tree


def build_both_trees(keyword, ngrams, frequencies):
    fwd_ngrams, fwd_frequencies = [], []
    bwd_ngrams, bwd_frequencies = [], []

    for ngram, freq in zip(ngrams, frequencies):
        fwd = ngram[0] == keyword
        bwd = ngram[-1] == keyword
        assert fwd or bwd, "ngram does not have keyword at beginning or end: {}".format(ngram)

        if fwd:
            fwd_ngrams.append(ngram[1:])
            fwd_frequencies.append(freq)
        if bwd:
            bwd_ngrams.append(reversed(ngram[:-1]))
            bwd_frequencies.append(freq)

    fwd_tree = build_tree(fwd_ngrams, fwd_frequencies)
    bwd_tree = build_tree(bwd_ngrams, bwd_frequencies)

    return fwd_tree, bwd_tree


class TreeDrawer:
    def __init__(self, keyword, fwd_tree, bwd_tree, max_font_size=30, min_font_size=12):
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.keyword = keyword
        self.fwd_tree = fwd_tree
        self.bwd_tree = bwd_tree
        self.max_freq = max([t.freq for t in fwd_tree.children.values()] +
                            [t.freq for t in bwd_tree.children.values()])

        self.graph = Digraph()
        self.graph.attr('graph', rankdir='LR')
        self.graph.attr('node', shape='plaintext', margin='0')

    def draw_subtree(self, tree, direction, root, suffix, depth):
        if depth > 0:
            lower = self.min_font_size
            upper = self.max_font_size
            fontsize = int(tree.freq / self.max_freq * (upper - lower) + lower)
            self.graph.node(root + suffix, label=root, fontsize=str(fontsize))

        for word, subtree in tree.children.items():
            new_suffix = '{}-{}'.format(suffix, word)
            self.draw_subtree(subtree, direction, word, new_suffix, depth + 1)
            src = root if depth == 0 else root + suffix
            dst = word + new_suffix
            if direction == Direction.Forward:
                self.graph.edge(src, dst)
            else:
                self.graph.edge(dst, src)

    def draw(self):
        self.graph.node(self.keyword,
                        label=self.keyword,
                        fontsize=str(self.max_font_size))
        self.draw_subtree(self.bwd_tree, Direction.Backward, self.keyword, "-bwd", 0)
        self.draw_subtree(self.fwd_tree, Direction.Forward, self.keyword, "-fwd", 0)
        return self.graph


def draw(keyword, ngrams, frequencies, **kwargs):
    fwd_tree, bwd_tree = build_both_trees(keyword, ngrams, frequencies)
    t = TreeDrawer(keyword, fwd_tree, bwd_tree, **kwargs)
    return t.draw()


def search_and_draw(corpus, keyword, max_n=5, tokenizer=None, **kwargs):
    if tokenizer is None:
        tokenizer = lambda s: [w.lower() for w in s.split(' ')]

    frequencies_dict = defaultdict(int)
    for doc in corpus:
        tokens = tokenizer(doc)
        for n in range(2, max_n + 1):
            for i in range(0, len(tokens) - n + 1):
                ngram = tokens[i:i + n]
                if ngram[0] == keyword or ngram[-1] == keyword:
                    frequencies_dict[tuple(ngram)] += 1

    ngrams = []
    frequencies = []
    for ngram, freq in frequencies_dict.items():
        ngrams.append(ngram)
        frequencies.append(freq)

    return draw(keyword, ngrams, frequencies, **kwargs)
