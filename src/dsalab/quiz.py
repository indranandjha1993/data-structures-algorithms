"""Checkpoint quizzes, one bank per module."""
import html
import ipywidgets as w
from IPython.display import display
from .common import is_static, caption

# Each question: text, options, index of the correct option, explanation.
QUESTIONS = {
    1: [
        ("Big-O notation describes",
         ["the exact running time in seconds", "how running time grows with input size, ignoring constants",
          "the memory a program uses", "how many lines of code an algorithm has"], 1,
         "Big-O keeps only the dominant term and drops constants: it is about the shape of growth, not the absolute time."),
        ("Binary search on one million sorted items needs at most about",
         ["1,000,000 comparisons", "1,000 comparisons", "20 comparisons", "2 comparisons"], 2,
         "Each comparison halves the range; log2(1,000,000) is about 20."),
        ("For large inputs, which running time is best?",
         ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"], 3,
         "Logarithmic growth barely notices the input size. The order from best to worst is log n, n, n log n, n^2."),
        ("Two nested loops that each run over all n items cost",
         ["O(n)", "O(2n)", "O(n^2)", "O(n log n)"], 2,
         "n iterations of the outer loop times n of the inner loop: n * n = n^2."),
    ],
    2: [
        ("Inserting at the front of a Python list of n items costs",
         ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 2,
         "Every existing element shifts one slot to the right. collections.deque does it in O(1)."),
        ("The main advantage of a linked list over an array is",
         ["faster access by index", "O(1) insertion or deletion at a known position, with no shifting",
          "less memory per element", "faster searching"], 1,
         "Linked lists only relink pointers. The price is O(n) access by index and extra memory per node."),
        ("Which structure processes items in the order they arrived?",
         ["a stack", "a queue", "a hash table", "a heap"], 1,
         "Queue = first in, first out. A stack is last in, first out."),
        ("collections.deque gives",
         ["O(1) append and pop at both ends", "O(1) access by index", "sorted order", "unique items only"], 0,
         "That is exactly why deque is the right choice for queues and sliding windows."),
    ],
    3: [
        ("Average cost of looking up a key in a hash table",
         ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 0,
         "Hashing jumps straight to the bucket. Only pathological collisions make it slower."),
        ("A collision happens when",
         ["two keys are equal", "two different keys land in the same bucket", "the table is full", "a key is deleted"], 1,
         "Collisions are normal; chaining or probing handles them. The load factor keeps them rare."),
        ("Which of these can NOT be a dict key in Python?",
         ["a string", "an integer", "a tuple of integers", "a list"], 3,
         "Keys must be hashable, which means immutable. Lists can change, so their hash would change."),
        ("When the load factor grows too high, a hash table",
         ["refuses new keys", "resizes to more buckets and rehashes every key", "switches to a linked list", "sorts its keys"], 1,
         "Resizing keeps chains short so lookups stay O(1) on average. It is O(n) once, amortised over many inserts."),
    ],
    4: [
        ("Every recursive function needs",
         ["a loop", "a base case that stops the recursion", "a global variable", "at least two arguments"], 1,
         "Without a base case the calls never stop and Python raises RecursionError."),
        ("Merge sort's running time is",
         ["O(n log n) in every case", "O(n^2) in the worst case", "O(n) on sorted input", "O(log n)"], 0,
         "It always splits in half and merges in linear time: log n levels of n work each."),
        ("Quicksort's worst case happens when",
         ["the input has duplicates", "the pivot is always the smallest or largest element", "n is odd", "the input is random"], 1,
         "A terrible pivot leaves one empty side, giving n levels of n work: O(n^2). Random pivots avoid it."),
        ("Python's built-in sorted() uses",
         ["bubble sort", "quicksort", "Timsort, a hybrid of merge sort and insertion sort", "heap sort"], 2,
         "Timsort is O(n log n), stable, and O(n) on already sorted input."),
    ],
    5: [
        ("The binary search tree property says",
         ["every node has exactly two children", "left subtree keys < node key < right subtree keys",
          "the tree is always balanced", "keys are stored in insertion order"], 1,
         "That ordering is what makes search a walk from the root: go left if smaller, right if larger."),
        ("In-order traversal of a BST visits keys in",
         ["insertion order", "random order", "sorted order", "reverse order"], 2,
         "Left, node, right: smallest first."),
        ("Inserting the keys 1, 2, 3, ..., n in that order into a plain BST gives height",
         ["log n", "n / 2", "n", "1"], 2,
         "Each key goes right of the previous one: a chain. Self-balancing trees fix this."),
        ("A binary min-heap guarantees",
         ["the smallest item is at the root", "the array is sorted", "O(1) search for any key", "no duplicates"], 0,
         "Only the root is special. Push and pop-min cost O(log n), which makes it a priority queue."),
    ],
    6: [
        ("Breadth-first search keeps its frontier in",
         ["a stack", "a queue", "a heap", "a set only"], 1,
         "A queue explores in rings of increasing distance. Depth-first search uses a stack (or recursion)."),
        ("In an unweighted graph, BFS from a start node finds",
         ["a shortest path (fewest edges) to every reachable node", "the cheapest weighted path", "all cycles", "a spanning tree of maximum weight"], 0,
         "The first time BFS reaches a node is along a path with the fewest edges."),
        ("Dijkstra's algorithm requires",
         ["a tree", "non-negative edge weights", "an undirected graph", "at most 100 nodes"], 1,
         "With negative weights a node popped from the heap could later be improved, breaking the argument."),
        ("An adjacency list for a graph with V vertices and E edges uses memory",
         ["O(V)", "O(V + E)", "O(V^2)", "O(E^2)"], 1,
         "One entry per vertex plus one per edge end. An adjacency matrix always uses O(V^2)."),
    ],
    7: [
        ("Dynamic programming pays off when a problem has",
         ["random inputs", "overlapping subproblems and optimal substructure", "no base case", "only one solution"], 1,
         "Overlapping subproblems mean naive recursion repeats work; storing results removes the repetition."),
        ("Memoization is",
         ["bottom-up table filling", "top-down recursion with a cache of results", "a sorting technique", "a kind of greedy choice"], 1,
         "Tabulation is the bottom-up twin. Both give the same complexity."),
        ("Naive recursive Fibonacci has running time about",
         ["O(n)", "O(n log n)", "O(2^n)", "O(n^2)"], 2,
         "Each call spawns two more. With a memo it becomes O(n)."),
        ("For coins {1, 4, 6} and amount 8, the greedy approach gives",
         ["2 coins, the optimum", "3 coins, worse than the optimum of 2", "4 coins", "no answer"], 1,
         "Greedy takes 6 then 1 then 1. DP finds 4 + 4. Greedy only works for special coin systems."),
    ],
}


class Quiz:
    def __init__(self, module):
        if module not in QUESTIONS:
            raise ValueError(f"no quiz for module {module}")
        self.module = module
        self.items = QUESTIONS[module]
        self.correct = 0
        self.answered = 0
        self._build_ui()

    def _build_ui(self):
        blocks = []
        self.score = w.HTML()
        for i, (text, options, answer, why) in enumerate(self.items, start=1):
            q = w.HTML(f"<b>Q{i}.</b> {html.escape(text)}")
            radio = w.RadioButtons(options=options, value=None, layout=w.Layout(width="auto"))
            check = w.Button(description="Check", layout=w.Layout(width="80px"))
            feedback = w.HTML()
            check.on_click(lambda _b, r=radio, c=check, f=feedback, a=answer, why=why, opts=options: self._check(r, c, f, a, why, opts))
            blocks.append(w.VBox([q, radio, w.HBox([check, feedback])], layout=w.Layout(margin="0 0 12px 0")))
        header = w.HTML(f"<b>Checkpoint quiz, Module {self.module}.</b> {len(self.items)} questions. Pick an answer and press Check.")
        self.ui = w.VBox([header] + blocks + [self.score])
        self._update_score()

    def _check(self, radio, check, feedback, answer, why, options):
        if radio.value is None:
            feedback.value = "<span style='color:#c00'>Pick an answer first.</span>"
            return
        chosen = options.index(radio.value)
        self.answered += 1
        if chosen == answer:
            self.correct += 1
            feedback.value = f"<span style='color:#080'><b>Correct.</b> {html.escape(why)}</span>"
        else:
            feedback.value = (f"<span style='color:#c00'><b>Not quite.</b> The answer is \"{html.escape(options[answer])}\". "
                              f"{html.escape(why)}</span>")
        radio.disabled = True
        check.disabled = True
        self._update_score()

    def _update_score(self):
        n = len(self.items)
        if self.answered == n:
            note = " Well done, move on." if self.correct == n else " Re-read the sections for the ones you missed before moving on."
            self.score.value = f"<b>Score: {self.correct} / {n}.</b>{note}"
        else:
            self.score.value = f"<b>Score so far: {self.correct} / {self.answered}</b> (of {n})"


def quiz(module, static=None):
    """Show the checkpoint quiz for a module (1 to 7)."""
    q = Quiz(module)
    if is_static(static):
        caption(f"Checkpoint quiz, Module {module} (static preview). Run this cell in JupyterLab to answer interactively.")
        for i, (text, options, _a, _w) in enumerate(q.items, start=1):
            caption(f"\nQ{i}. {text}")
            for j, opt in enumerate(options):
                caption(f"    {'abcd'[j]}) {opt}")
        return None
    display(q.ui)
    return None
