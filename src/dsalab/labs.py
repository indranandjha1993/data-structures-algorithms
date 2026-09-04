"""Interactive labs: sorting visualiser, binary search stepper, BST builder, graph explorer,
hash table lab, edit distance lab and coin change lab."""
import random
from collections import deque
import ipywidgets as w
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from .common import is_static, caption, display_static, show_in, close_if_inline
from .viz import draw_array, draw_tree, draw_graph, draw_table


# ---------------------------------------------------------------------------
# Sorting visualiser
# ---------------------------------------------------------------------------
def bubble_steps(a):
    a = list(a)
    yield list(a)
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                yield list(a)


def insertion_steps(a):
    a = list(a)
    yield list(a)
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j - 1] > a[j]:
            a[j - 1], a[j] = a[j], a[j - 1]
            j -= 1
            yield list(a)


def _merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def merge_steps(a):
    a = list(a)
    yield list(a)

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        yield from sort(lo, mid)
        yield from sort(mid, hi)
        a[lo:hi] = _merge(a[lo:mid], a[mid:hi])
        yield list(a)

    yield from sort(0, len(a))


def quick_steps(a):
    a = list(a)
    yield list(a)

    def sort(lo, hi):
        if lo >= hi:
            return
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
                yield list(a)
        a[i], a[hi] = a[hi], a[i]
        yield list(a)
        yield from sort(lo, i - 1)
        yield from sort(i + 1, hi)

    yield from sort(0, len(a) - 1)


ALGORITHMS = {"bubble": bubble_steps, "insertion": insertion_steps, "merge": merge_steps, "quick": quick_steps}


class SortingVisualizer:
    def __init__(self, n=20, seed=7):
        self.n, self.seed = n, seed
        self._new_array()
        self._build_ui()
        self._render()

    def _new_array(self):
        rng = random.Random(self.seed)
        self.arr = rng.sample(range(1, self.n + 1), self.n)
        self.frames = {name: list(fn(self.arr)) for name, fn in ALGORITHMS.items()}

    def figure(self, algo, k):
        frames = self.frames[algo]
        k = min(k, len(frames) - 1)
        state, target = frames[k], sorted(self.arr)
        fig, ax = plt.subplots(figsize=(8.5, 3))
        ax.bar(range(len(state)), state, color=["tab:green" if state[i] == target[i] else "tab:blue" for i in range(len(state))])
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"{algo} sort, step {k} of {len(frames) - 1}   (green = already in its final place)", fontsize=10)
        return close_if_inline(fig)

    def counts_html(self):
        parts = [f"{name}: {len(fr) - 1} swaps/writes" for name, fr in self.frames.items()]
        return "<span style='font-family:monospace; font-size:12px'>" + " &nbsp;|&nbsp; ".join(parts) + "</span>"

    def _build_ui(self):
        self.algo = w.Dropdown(options=list(ALGORITHMS), value="bubble", description="algorithm", layout=w.Layout(width="200px"))
        self.k = w.IntSlider(value=0, min=0, max=len(self.frames["bubble"]) - 1, step=1, description="step", continuous_update=False, layout=w.Layout(width="360px"))
        self.play = w.Play(value=0, min=0, max=self.k.max, step=1, interval=120, description="play")
        w.jslink((self.play, "value"), (self.k, "value"))
        self.size = w.IntSlider(value=self.n, min=5, max=40, step=1, description="items", continuous_update=False, layout=w.Layout(width="260px"))
        shuffle = w.Button(description="Shuffle", layout=w.Layout(width="90px"))
        self.counts = w.HTML(self.counts_html())
        self.out = w.Output()
        self.algo.observe(lambda ch: self._on_algo(), names="value")
        self.k.observe(lambda ch: self._render(), names="value")
        self.size.observe(lambda ch: self._on_size(ch["new"]), names="value")
        shuffle.on_click(lambda _b: self._on_shuffle())
        header = w.HTML("<b>Sorting Visualiser.</b> Press play or drag the step slider. Compare how many steps each algorithm takes on the same input.")
        self.ui = w.VBox([header, w.HBox([self.algo, self.size, shuffle]), w.HBox([self.play, self.k]), self.out, self.counts])

    def _on_algo(self):
        self.k.max = self.play.max = len(self.frames[self.algo.value]) - 1
        self.k.value = 0
        self._render()

    def _on_size(self, n):
        self.n = n
        self._new_array()
        self._on_algo()
        self.counts.value = self.counts_html()

    def _on_shuffle(self):
        self.seed += 1
        self._new_array()
        self._on_algo()
        self.counts.value = self.counts_html()

    def _render(self):
        show_in(self.out, self.figure(self.algo.value, self.k.value))


def sorting_visualizer(n=20, seed=7, static=None):
    """Open the Sorting Visualiser."""
    lab = SortingVisualizer(n, seed)
    if is_static(static):
        caption("Sorting Visualiser (static preview). Run this cell in JupyterLab for the interactive version.")
        display_static(lab.figure("bubble", 0), lab.figure("quick", 12))
        display(HTML(lab.counts_html()))
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# Binary search stepper
# ---------------------------------------------------------------------------
def binary_search_trace(items, target):
    lo, hi, steps = 0, len(items) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append((lo, mid, hi))
        if items[mid] == target:
            return steps, mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps, -1


class BinarySearchStepper:
    def __init__(self, n=24, seed=3):
        rng = random.Random(seed)
        self.items = sorted(rng.sample(range(1, 99), n))
        self.missing = next(v for v in range(1, 99) if v not in self.items)
        self._build_ui()
        self._on_target()

    def figure(self, k):
        steps, found = self.steps, self.found
        target = self.target.value
        if k == 0:
            return draw_array(self.items, title=f"looking for {target}: the whole array is in play")
        lo, mid, hi = steps[k - 1]
        highlight = {i: "#eeeeee" for i in range(len(self.items)) if i < lo or i > hi}
        highlight[mid] = "tab:orange"
        labels = {lo: "lo", hi: "hi"}
        labels[mid] = "mid" if mid not in (lo, hi) else labels[mid] + "/mid"
        v = self.items[mid]
        if v == target:
            highlight[mid] = "tab:green"
            text = f"step {k}: items[{mid}] = {v} equals {target}. Found."
        elif v < target:
            text = f"step {k}: items[{mid}] = {v} < {target}, so discard everything left of mid."
        else:
            text = f"step {k}: items[{mid}] = {v} > {target}, so discard everything right of mid."
        if k == len(steps) and found == -1:
            text += " Range is empty: not present."
        return draw_array(self.items, highlight=highlight, labels=labels, title=text)

    def _build_ui(self):
        self.target = w.Dropdown(options=self.items + [self.missing], value=self.items[-3], description="target", layout=w.Layout(width="160px"))
        self.k = w.IntSlider(value=0, min=0, max=1, step=1, description="step", continuous_update=False, layout=w.Layout(width="300px"))
        prev = w.Button(description="Prev", layout=w.Layout(width="70px"))
        nxt = w.Button(description="Next", button_style="primary", layout=w.Layout(width="70px"))
        self.info = w.HTML()
        self.out = w.Output()
        self.target.observe(lambda ch: self._on_target(), names="value")
        self.k.observe(lambda ch: self._render(), names="value")
        prev.on_click(lambda _b: setattr(self.k, "value", max(0, self.k.value - 1)))
        nxt.on_click(lambda _b: setattr(self.k, "value", min(self.k.max, self.k.value + 1)))
        header = w.HTML("<b>Binary Search Stepper.</b> Pick a target and step through the comparisons. Grey cells are ruled out.")
        self.ui = w.VBox([header, w.HBox([self.target, prev, nxt, self.k]), self.out, self.info])

    def _on_target(self):
        self.steps, self.found = binary_search_trace(self.items, self.target.value)
        self.k.max = len(self.steps)
        self.k.value = 0
        self._render()

    def _render(self):
        show_in(self.out, self.figure(self.k.value))
        n = len(self.items)
        self.info.value = (f"<span style='font-family:monospace; font-size:12px'>{n} items: binary search needs at most "
                           f"{n.bit_length()} comparisons, linear search up to {n}. This target: {len(self.steps)} comparisons.</span>")


def binary_search_stepper(n=24, seed=3, static=None):
    """Open the Binary Search Stepper."""
    lab = BinarySearchStepper(n, seed)
    if is_static(static):
        caption("Binary Search Stepper (static preview). Run this cell in JupyterLab for the interactive version.")
        display_static(*[lab.figure(k) for k in range(min(3, len(lab.steps) + 1))])
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# BST builder
# ---------------------------------------------------------------------------
class TreeNode:
    __slots__ = ("value", "left", "right")

    def __init__(self, value):
        self.value, self.left, self.right = value, None, None


def bst_insert(root, value):
    if root is None:
        return TreeNode(value)
    cur = root
    while True:
        if value < cur.value:
            if cur.left is None:
                cur.left = TreeNode(value); break
            cur = cur.left
        elif value > cur.value:
            if cur.right is None:
                cur.right = TreeNode(value); break
            cur = cur.right
        else:
            break  # duplicates ignored
    return root


def bst_search_path(root, value):
    path, cur = [], root
    while cur is not None:
        path.append(cur)
        if value == cur.value:
            return path, True
        cur = cur.left if value < cur.value else cur.right
    return path, False


def bst_height(node):
    return 0 if node is None else 1 + max(bst_height(node.left), bst_height(node.right))


def bst_inorder(node):
    if node is not None:
        yield from bst_inorder(node.left)
        yield node.value
        yield from bst_inorder(node.right)


class BSTBuilder:
    def __init__(self, values=None):
        self.root = None
        self.values = []
        self.path = []
        for v in (values or []):
            self.insert(v)
        self._build_ui()
        self._render()

    def insert(self, v):
        self.root = bst_insert(self.root, v)
        self.values.append(v)
        self.path = []

    def figure(self):
        n = len(list(bst_inorder(self.root)))
        title = f"{n} keys, height {bst_height(self.root)}" + (f", ideal height about {max(1, n.bit_length())}" if n else "")
        return draw_tree(self.root, lambda t: (t.left, t.right), lambda t: str(t.value), title=title, highlight=self.path)

    def info_html(self):
        keys = list(bst_inorder(self.root))
        return (f"<span style='font-family:monospace; font-size:12px'>insertion order: {self.values}<br>"
                f"in-order traversal: {keys}</span>")

    def _build_ui(self):
        self.value = w.IntText(value=50, description="value", layout=w.Layout(width="160px"))
        ins = w.Button(description="Insert", button_style="primary", layout=w.Layout(width="80px"))
        rnd = w.Button(description="Insert 10 random", layout=w.Layout(width="140px"))
        srt = w.Button(description="Insert 1..10 sorted", layout=w.Layout(width="150px"))
        clr = w.Button(description="Clear", button_style="danger", layout=w.Layout(width="80px"))
        self.search = w.IntText(value=50, description="search", layout=w.Layout(width="160px"))
        srch = w.Button(description="Search", layout=w.Layout(width="80px"))
        self.status = w.HTML()
        self.info = w.HTML()
        self.out = w.Output()
        ins.on_click(lambda _b: (self.insert(self.value.value), self._render()))
        rnd.on_click(lambda _b: self._on_random())
        srt.on_click(lambda _b: ([self.insert(v) for v in range(1, 11)], self._render()))
        clr.on_click(lambda _b: self._on_clear())
        srch.on_click(lambda _b: self._on_search())
        header = w.HTML("<b>BST Builder.</b> Insert keys and watch the tree grow. Search highlights the path from the root. "
                        "Compare random insertion with sorted insertion.")
        self.ui = w.VBox([header, w.HBox([self.value, ins, rnd, srt, clr]), w.HBox([self.search, srch, self.status]), self.out, self.info])

    def _on_random(self):
        rng = random.Random()
        for v in rng.sample(range(1, 100), 10):
            self.insert(v)
        self._render()

    def _on_clear(self):
        self.root, self.values, self.path = None, [], []
        self.status.value = ""
        self._render()

    def _on_search(self):
        self.path, found = bst_search_path(self.root, self.search.value)
        self.status.value = (f"<span style='color:#080'>found after {len(self.path)} comparisons</span>" if found
                             else f"<span style='color:#c00'>not present, {len(self.path)} comparisons</span>")
        self._render()

    def _render(self):
        show_in(self.out, self.figure())
        self.info.value = self.info_html()


def bst_builder(values=None, static=None):
    """Open the BST Builder, optionally pre-loaded with a list of keys."""
    lab = BSTBuilder(values)
    if is_static(static):
        caption("BST Builder (static preview). Run this cell in JupyterLab for the interactive version.")
        display_static(lab.figure())
        display(HTML(lab.info_html()))
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# Graph explorer
# ---------------------------------------------------------------------------
GRAPHS = {
    "small": {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"], "D": ["B"], "E": ["B", "F"], "F": ["C", "E", "G"], "G": ["F"]},
    "ring with a chord": {"1": ["2", "8"], "2": ["1", "3"], "3": ["2", "4", "7"], "4": ["3", "5"], "5": ["4", "6"], "6": ["5", "7"], "7": ["6", "8", "3"], "8": ["7", "1"]},
    "two components": {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"], "X": ["Y"], "Y": ["X", "Z"], "Z": ["Y"]},
}


def bfs_trace(graph, start):
    # Each step: (current node, visited order so far, frontier after the step)
    visited, order, queue, steps = {start}, [], deque([start]), []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
        steps.append((node, list(order), list(queue)))
    return steps


def dfs_trace(graph, start):
    visited, order, stack, steps = set(), [], [start], []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for nb in reversed(graph[node]):
            if nb not in visited:
                stack.append(nb)
        steps.append((node, list(order), list(stack)))
    return steps


class GraphExplorer:
    def __init__(self, graph="small", algorithm="BFS"):
        self._build_ui(graph, algorithm)
        self._recompute()

    def figure(self, k):
        graph = GRAPHS[self.graph_dd.value]
        if k == 0:
            return draw_graph(graph, node_colors={self.start.value: "tab:orange"}, title="before the first step")
        node, order, frontier = self.steps[k - 1]
        colors = {v: "#f0c419" for v in frontier}
        colors[node] = "tab:orange"
        prev = order[:-1]
        for v in prev:
            colors[v] = plt.cm.viridis(order.index(v) / max(1, len(graph) - 1))
        label = "queue" if self.algo.value == "BFS" else "stack"
        return draw_graph(graph, order=None, node_colors=colors,
                          title=f"step {k}: visiting {node}   {label} = {frontier}   visited = {order}")

    def _build_ui(self, graph, algorithm):
        self.graph_dd = w.Dropdown(options=list(GRAPHS), value=graph, description="graph", layout=w.Layout(width="220px"))
        self.start = w.Dropdown(options=list(GRAPHS[graph]), description="start", layout=w.Layout(width="140px"))
        self.algo = w.Dropdown(options=["BFS", "DFS"], value=algorithm, description="algorithm", layout=w.Layout(width="170px"))
        self.k = w.IntSlider(value=0, min=0, max=1, step=1, description="step", continuous_update=False, layout=w.Layout(width="300px"))
        prev = w.Button(description="Prev", layout=w.Layout(width="70px"))
        nxt = w.Button(description="Next", button_style="primary", layout=w.Layout(width="70px"))
        self.out = w.Output()
        self.graph_dd.observe(lambda ch: self._on_graph(), names="value")
        self.start.observe(lambda ch: self._recompute(), names="value")
        self.algo.observe(lambda ch: self._recompute(), names="value")
        self.k.observe(lambda ch: self._render(), names="value")
        prev.on_click(lambda _b: setattr(self.k, "value", max(0, self.k.value - 1)))
        nxt.on_click(lambda _b: setattr(self.k, "value", min(self.k.max, self.k.value + 1)))
        header = w.HTML("<b>Graph Explorer.</b> Step through BFS or DFS. Orange = node being visited, yellow = waiting in the queue or stack, "
                        "coloured = already visited (darker = earlier).")
        self.ui = w.VBox([header, w.HBox([self.graph_dd, self.start, self.algo]), w.HBox([prev, nxt, self.k]), self.out])

    def _on_graph(self):
        self.start.options = list(GRAPHS[self.graph_dd.value])
        self.start.value = self.start.options[0]
        self._recompute()

    def _recompute(self):
        graph = GRAPHS[self.graph_dd.value]
        fn = bfs_trace if self.algo.value == "BFS" else dfs_trace
        self.steps = fn(graph, self.start.value)
        self.k.max = len(self.steps)
        self.k.value = 0
        self._render()

    def _render(self):
        show_in(self.out, self.figure(self.k.value))


def graph_explorer(graph="small", algorithm="BFS", static=None):
    """Open the Graph Explorer."""
    lab = GraphExplorer(graph, algorithm)
    if is_static(static):
        caption("Graph Explorer (static preview). Run this cell in JupyterLab for the interactive version.")
        display_static(lab.figure(0), lab.figure(3))
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# Hash table lab
# ---------------------------------------------------------------------------
class HashTableLab:
    def __init__(self, buckets=8, keys=12, seed=1):
        self._build_ui(buckets, keys, seed)
        self._render()

    def stats(self):
        m, n = self.m.value, self.n.value
        rng = random.Random(self.seed.value)
        keys = rng.sample(range(1000, 9999), n)
        if self.resize.value:
            while n / m > 0.75:
                m *= 2
        occupancy = [0] * m
        collisions = 0
        for k in keys:
            b = k % m
            if occupancy[b]:
                collisions += 1
            occupancy[b] += 1
        return m, keys, occupancy, collisions

    def figure(self):
        m, keys, occ, collisions = self.stats()
        fig, ax = plt.subplots(figsize=(max(6, 0.22 * m), 3))
        ax.bar(range(m), occ, color=["tab:red" if o > 1 else ("tab:blue" if o == 1 else "#dddddd") for o in occ])
        ax.set_xlabel("bucket = key mod m"); ax.set_ylabel("keys in bucket")
        ax.set_title(f"{len(keys)} keys into {m} buckets: load factor {len(keys)/m:.2f}, {collisions} collisions, "
                     f"longest chain {max(occ)}, empty buckets {occ.count(0)}", fontsize=10)
        ax.set_yticks(range(0, max(occ) + 1))
        fig.tight_layout()
        return close_if_inline(fig)

    def _build_ui(self, buckets, keys, seed):
        self.m = w.IntSlider(value=buckets, min=2, max=64, step=1, description="buckets m", continuous_update=False, layout=w.Layout(width="300px"))
        self.n = w.IntSlider(value=keys, min=1, max=120, step=1, description="keys n", continuous_update=False, layout=w.Layout(width="300px"))
        self.seed = w.IntSlider(value=seed, min=0, max=20, step=1, description="seed", continuous_update=False, layout=w.Layout(width="220px"))
        self.resize = w.Checkbox(value=False, description="resize when load factor > 0.75", indent=False)
        self.out = w.Output()
        for widget in (self.m, self.n, self.seed, self.resize):
            widget.observe(lambda ch: self._render(), names="value")
        header = w.HTML("<b>Hash Table Lab.</b> Random integer keys go into bucket (key mod m). Red bars are collisions. "
                        "Push n up and watch chains grow, then switch on resizing.")
        self.ui = w.VBox([header, w.HBox([self.m, self.n]), w.HBox([self.seed, self.resize]), self.out])

    def _render(self):
        show_in(self.out, self.figure())


def hash_table_lab(buckets=8, keys=12, seed=1, static=None):
    """Open the Hash Table Lab."""
    lab = HashTableLab(buckets, keys, seed)
    if is_static(static):
        caption("Hash Table Lab (static preview). Run this cell in JupyterLab for the interactive version.")
        display_static(lab.figure())
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# Edit distance lab
# ---------------------------------------------------------------------------
def edit_distance_table(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d


def edit_distance_path(a, b, d):
    i, j, path, ops = len(a), len(b), [], []
    while i > 0 or j > 0:
        path.append((i, j))
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1):
            ops.append("keep " + a[i - 1] if a[i - 1] == b[j - 1] else f"replace {a[i - 1]} with {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            ops.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            ops.append(f"insert {b[j - 1]}")
            j -= 1
    path.append((0, 0))
    return path, list(reversed(ops))


class EditDistanceLab:
    def __init__(self, a="kitten", b="sitting"):
        self._build_ui(a, b)
        self._render()

    def figure(self):
        a, b = self.a.value, self.b.value
        d = edit_distance_table(a, b)
        path, ops = edit_distance_path(a, b, d)
        fig = draw_table(d, [""] + list(a), [""] + list(b), title=f"edit distance('{a}', '{b}') = {d[len(a)][len(b)]}", highlight=path)
        return fig, ops

    def _build_ui(self, a, b):
        self.a = w.Text(value=a, description="word A", layout=w.Layout(width="220px"))
        self.b = w.Text(value=b, description="word B", layout=w.Layout(width="220px"))
        self.ops = w.HTML()
        self.out = w.Output()
        self.a.observe(lambda ch: self._render(), names="value")
        self.b.observe(lambda ch: self._render(), names="value")
        header = w.HTML("<b>Edit Distance Lab.</b> Each cell holds the cheapest way to turn a prefix of A into a prefix of B. "
                        "The red path is the answer read backwards from the bottom-right corner.")
        self.ui = w.VBox([header, w.HBox([self.a, self.b]), self.out, self.ops])

    def _render(self):
        fig, ops = self.figure()
        show_in(self.out, fig)
        self.ops.value = "<span style='font-family:monospace; font-size:12px'>" + " , ".join(o for o in ops if not o.startswith("keep")) + "</span>"


def edit_distance_lab(a="kitten", b="sitting", static=None):
    """Open the Edit Distance Lab."""
    lab = EditDistanceLab(a, b)
    if is_static(static):
        caption("Edit Distance Lab (static preview). Run this cell in JupyterLab for the interactive version.")
        fig, ops = lab.figure()
        display_static(fig)
        display(HTML("<span style='font-family:monospace; font-size:12px'>" + " , ".join(o for o in ops if not o.startswith("keep")) + "</span>"))
        return None
    display(lab.ui)
    return None


# ---------------------------------------------------------------------------
# Coin change lab
# ---------------------------------------------------------------------------
def min_coins(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    choice = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                choice[a] = c
    used, a = [], amount
    while a > 0 and choice[a] is not None:
        used.append(choice[a])
        a -= choice[a]
    return dp, used


def greedy_coins(coins, amount):
    used = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            used.append(c)
            amount -= c
    return used if amount == 0 else None


class CoinChangeLab:
    def __init__(self, coins=(1, 4, 6), amount=8):
        self._build_ui(coins, amount)
        self._render()

    def parse_coins(self):
        try:
            coins = sorted({int(x) for x in self.coins.value.replace(" ", "").split(",") if x})
            return coins if coins and all(c > 0 for c in coins) else None
        except ValueError:
            return None

    def figure(self):
        coins, amount = self.parse_coins(), self.amount.value
        if not coins:
            return None, "<span style='color:#c00'>coins must be positive integers separated by commas</span>"
        dp, used = min_coins(coins, amount)
        greedy = greedy_coins(coins, amount)
        fig, ax = plt.subplots(figsize=(9, 3))
        vals = [v if v != float("inf") else 0 for v in dp]
        ax.bar(range(amount + 1), vals, color=["tab:orange" if a == amount else "tab:blue" for a in range(amount + 1)])
        ax.set_xlabel("amount"); ax.set_ylabel("min coins")
        ax.set_title(f"dp[a] = fewest coins for amount a, coins {coins}", fontsize=10)
        fig.tight_layout()
        dp_txt = f"DP: {len(used)} coins {sorted(used, reverse=True)}" if dp[amount] != float("inf") else "DP: impossible"
        g_txt = f"greedy (largest coin first): {len(greedy)} coins {greedy}" if greedy else "greedy: gets stuck"
        verdict = ""
        if greedy and dp[amount] != float("inf") and len(greedy) > len(used):
            verdict = " <b>Greedy is wrong here.</b>"
        return close_if_inline(fig), f"<span style='font-family:monospace; font-size:12px'>{dp_txt} &nbsp;|&nbsp; {g_txt}{verdict}</span>"

    def _build_ui(self, coins, amount):
        self.coins = w.Text(value=", ".join(str(c) for c in coins), description="coins", layout=w.Layout(width="240px"))
        self.amount = w.IntSlider(value=amount, min=1, max=40, step=1, description="amount", continuous_update=False, layout=w.Layout(width="320px"))
        self.info = w.HTML()
        self.out = w.Output()
        self.coins.observe(lambda ch: self._render(), names="value")
        self.amount.observe(lambda ch: self._render(), names="value")
        header = w.HTML("<b>Coin Change Lab.</b> The table builds up from amount 0. Compare the optimal answer with the greedy one.")
        self.ui = w.VBox([header, w.HBox([self.coins, self.amount]), self.out, self.info])

    def _render(self):
        fig, html = self.figure()
        show_in(self.out, fig)
        self.info.value = html


def coin_change_lab(coins=(1, 4, 6), amount=8, static=None):
    """Open the Coin Change Lab."""
    lab = CoinChangeLab(coins, amount)
    if is_static(static):
        caption("Coin Change Lab (static preview). Run this cell in JupyterLab for the interactive version.")
        fig, html = lab.figure()
        display_static(fig)
        display(HTML(html))
        return None
    display(lab.ui)
    return None
