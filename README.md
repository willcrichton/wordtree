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
documents = ["hello world", "world is my oyster"]
g = search_and_draw(corpus = documents, keyword = "world")
g.render() # creates a file world.dv.png
```

## API documentation

This library has two main functions: `search`, which counts phrase ("N-gram") frequency in a corpus, and `draw`, which generates a word tree diagram from the N-gram frequencies. `search_and_draw` naturally combines the two together.
