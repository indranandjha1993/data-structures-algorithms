# Data Structures and Algorithms

[![Read online](https://img.shields.io/badge/read%20online-github%20pages-blue)](https://indranandjha1993.github.io/data-structures-algorithms/) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/indranandjha1993/data-structures-algorithms/main?urlpath=lab/tree/src/00_Start_Here.ipynb)

A hands-on, eight-notebook course in data structures and algorithms. Every idea is introduced three ways:
as a **picture** of the structure, as **Python code short enough to read in one screen**, and as a
**measurement** on your own machine, so Big-O claims are checked with timing plots rather than taken on faith.

## Read or run it

- **Read online:** https://indranandjha1993.github.io/data-structures-algorithms/ is the full course as a website, built from these notebooks on every push.
- **Run online:** the Binder badge above opens the notebooks in a live JupyterLab in your browser, labs included. The first launch after a change takes a few minutes while the image builds; later launches are quick.
- **Run locally:** see Setup below.

## Course map

Start with `src/00_Start_Here.ipynb`: it checks your environment, introduces the helpers and labs, and
links to every module.

| # | Notebook | What you learn |
|---|----------|----------------|
| 0 | `00_Start_Here` | Setup check, the toolkit, cost cheat sheets, glossary |
| 1 | `01_Complexity_and_Big_O` | Counting steps, Big-O rules, timing plots, best/worst/amortised cost |
| 2 | `02_Arrays_Linked_Lists_Stacks_Queues` | Dynamic arrays, linked lists, stacks, queues, the call stack |
| 3 | `03_Hash_Tables_and_Sets` | Hashing, chaining, load factor, why dict and set are fast |
| 4 | `04_Recursion_Searching_and_Sorting` | Recursion, divide and conquer, binary search, four sorts compared |
| 5 | `05_Trees_and_Heaps` | Binary search trees, balance, traversals, heaps and priority queues |
| 6 | `06_Graphs` | Adjacency lists, BFS, DFS, grid mazes, Dijkstra, topological order |
| 7 | `07_Dynamic_Programming` | Memoisation vs tabulation, coin change, edit distance, knapsack |

Each module has learning objectives, "what to notice" callouts after every experiment, an interactive lab,
exercises with hidden solutions, a checkpoint quiz and key takeaways.

## Interactive labs

Seven simulators live in `src/dsalab/` and are wired into the modules. Each needs a running kernel; viewed
statically the notebooks show a preview of the initial state instead.

| Lab | Used in | What you do |
|-----|---------|-------------|
| Binary Search Stepper | Module 1 | Step through the comparisons and watch the range shrink. |
| Hash Table Lab | Module 3 | Pour keys into buckets, watch collisions grow, switch on resizing. |
| Sorting Visualiser | Module 4 | Play bubble, insertion, merge and quick sort on the same input and count their steps. |
| BST Builder | Module 5 | Insert keys, search with the path highlighted, compare random and sorted insertion. |
| Graph Explorer | Module 6 | Step through BFS and DFS with the queue or stack shown. |
| Coin Change Lab | Module 7 | Build the DP table and watch greedy fail. |
| Edit Distance Lab | Module 7 | Type two words and see the table and the path through it. |

```python
from dsalab import time_it, growth_plot, draw_array, draw_linked_list, draw_tree, draw_graph, draw_grid, draw_table
from dsalab import sorting_visualizer, binary_search_stepper, bst_builder, graph_explorer
from dsalab import hash_table_lab, edit_distance_lab, coin_change_lab, quiz
```

The import works because Jupyter starts a notebook's kernel in the notebook's own folder. If you run a notebook
from elsewhere, add `src/` to `sys.path` first.

## Setup

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                                                    # creates .venv with numpy, matplotlib, ipywidgets
uv run python -m ipykernel install --user --name data_structures_algorithms
jupyter lab src/                                                           # then pick the data_structures_algorithms kernel
```

Notebooks ship with outputs, so you can read them without running anything. Timing cells take a few
seconds each; the numbers depend on your machine, the shapes of the curves do not.

## Editing the course

The notebooks are the source of truth: edit them directly in JupyterLab. If you add or reorder modules,
keep the navigation links at the top and bottom of each notebook pointing at the right neighbours and at
`00_Start_Here.ipynb`, and update the course map there and in this README.

## Related courses

This is one of three hands-on notebook courses built in the same format:

- [Quantum Computing with Code](https://github.com/indranandjha1993/quantum-computing): qubits to Grover and noise, with Qiskit
- [Design Patterns](https://github.com/indranandjha1993/design-patterns): the 23 Gang of Four patterns and the architectures they live in

## License

MIT. Use it, fork it, teach with it.
