# wordtree

This Python library generates word tree diagrams. Word tree diagrams show how often different phrases occur in a corpus that contain a specific keyword. For example, here's the keyword "dog" in the [Amazon Pet Supplies review corpus](http://jmcauley.ucsd.edu/data/amazon/):

![](https://github.com/willcrichton/wordtree/raw/master/static/dog.png)

## Installation

You need to have Graphviz installed on your machine. See the [Graphviz website](https://www.graphviz.org/download/) for instructions. Then, you can do:

```
pip install wordtree
```

## Example usage

```python
import wordtree
documents = ["hello world", "world is my oyster"]
g = wordtree.search_and_draw(corpus = documents, keyword = "world")
g.render() # creates a file world.dv.png
```

## API documentation

This library has two main functions: `search`, which counts phrase ("N-gram") frequency in a corpus, and `draw`, which generates a word tree diagram from the N-gram frequencies. `search_and_draw` naturally combines the two together.

### search

Required arguments:

* `corpus`: list of strings to search through
* `keyword`: single word that sits at the center of keyword tree

Optional arguments:

* `max_n`: maximum size of an N-gram to consider, e.g. `max_n = 5` means only show phrases up to 5 words in length
* `tokenize`: a function from a string to list of strings, cutting a document into words. By default, just splits on space.

Returns:

* `ngrams`: list of N-grams as tuples
* `frequencies`: parallel list of frequency count for each N-gram

### draw

Required arguments:

* `keyword`: single word that sits at the center of keyword tree
* `ngrams`: list of N-grams as tuples, e.g. `[("a", "b"), ("b", "c")]`
* `frequencies`: list of frequency counts, e.g. `[1, 3]`

Optional arguments:

* `max_per_n`: put up to this many N-grams into the final diagram per side per value of N. For example, if `max_per_n = 3`, then each side of the diagram will have no more than 3 N-grams of length 1, 2, 3, etc.
* `max_font_size` and `min_font_size`: bounds for font sizes in the diagram
* `font_interp`: function for interpolation between max and min font sizes given word frequency. Must be a real-valued function from `[0, 1] -> [0, 1]` where an input of 1 means "highest frequency in corpus" and 0 means "lowest frequency in corpus". Defaults to cube root
