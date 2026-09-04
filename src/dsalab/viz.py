"""Drawing helpers for arrays, linked lists, trees, graphs and grids."""
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from .common import close_if_inline

BOX = "#dfe7f5"


def draw_array(values, highlight=None, title="", labels=None):
    # highlight: {index: colour}. labels: optional {index: text} drawn under the cell (e.g. 'lo', 'mid').
    n = max(1, len(values))
    fig, ax = plt.subplots(figsize=(max(4, 0.6 * n), 1.9))
    for i, v in enumerate(values):
        color = (highlight or {}).get(i, BOX)
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor="k"))
        ax.text(i + 0.5, 0.5, str(v), ha="center", va="center", fontsize=9)
        ax.text(i + 0.5, -0.22, str(i), ha="center", va="center", fontsize=7, color="gray")
        if labels and i in labels:
            ax.text(i + 0.5, 1.22, labels[i], ha="center", va="center", fontsize=8, color="tab:red")
    ax.set_xlim(-0.1, n + 0.1)
    ax.set_ylim(-0.5, 1.5)
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    return close_if_inline(fig)


def draw_linked_list(values, title="", highlight=None):
    values = list(values)
    n = len(values)
    fig, ax = plt.subplots(figsize=(max(4, 1.3 * n + 1.2), 1.5))
    ax.text(-0.15, 0.3, "head", ha="right", va="center", fontsize=9, color="gray")
    for i, v in enumerate(values):
        x = i * 1.3
        color = (highlight or {}).get(i, BOX)
        ax.add_patch(plt.Rectangle((x, 0), 0.6, 0.6, facecolor=color, edgecolor="k"))
        ax.add_patch(plt.Rectangle((x + 0.6, 0), 0.3, 0.6, facecolor="white", edgecolor="k"))
        ax.text(x + 0.3, 0.3, str(v), ha="center", va="center", fontsize=9)
        ax.annotate("", xy=(x + 1.3, 0.3), xytext=(x + 0.75, 0.3), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(n * 1.3, 0.3, "None", va="center", fontsize=9)
    ax.set_xlim(-0.8, n * 1.3 + 0.9)
    ax.set_ylim(-0.3, 0.9)
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    return close_if_inline(fig)


def tree_positions(root, children):
    # x = in-order rank, y = -depth. Works for any binary tree whose nodes are hashable.
    pos = {}
    counter = [0]

    def visit(node, depth):
        if node is None:
            return
        left, right = children(node)
        visit(left, depth + 1)
        pos[node] = (counter[0], -depth)
        counter[0] += 1
        visit(right, depth + 1)

    visit(root, 0)
    return pos


def draw_tree(root, children, label, title="", highlight=(), figsize=None):
    if root is None:
        fig, ax = plt.subplots(figsize=(3, 1))
        ax.text(0.5, 0.5, "(empty tree)", ha="center", va="center")
        ax.axis("off")
        ax.set_title(title, fontsize=10)
        return close_if_inline(fig)
    pos = tree_positions(root, children)
    n = len(pos)
    depth = max(-y for _, y in pos.values()) + 1
    fig, ax = plt.subplots(figsize=figsize or (max(4, 0.75 * n), max(2.4, 0.85 * depth)))
    highlight = set(highlight)

    def visit(node):
        x, y = pos[node]
        for child in children(node):
            if child is not None:
                cx, cy = pos[child]
                ax.plot([x, cx], [y, cy], color="gray", lw=1.2, zorder=1)
                visit(child)
        ax.scatter([x], [y], s=520, color="tab:orange" if node in highlight else "tab:blue", zorder=2)
        ax.text(x, y, label(node), ha="center", va="center", color="white", fontsize=9, zorder=3)

    visit(root)
    ax.set_xlim(-1, n)
    ax.set_ylim(-depth + 0.4, 0.7)
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    return close_if_inline(fig)


def graph_layout(nodes):
    n = len(nodes)
    return {v: (math.cos(2 * math.pi * i / n + math.pi / 2), math.sin(2 * math.pi * i / n + math.pi / 2))
            for i, v in enumerate(nodes)}


def draw_graph(graph, order=None, path=None, weighted=False, title="", pos=None, node_colors=None, size=4.6):
    # graph: {node: [neighbours]} or {node: {neighbour: weight}} when weighted.
    nodes = list(graph)
    pos = pos or graph_layout(nodes)
    fig, ax = plt.subplots(figsize=(size, size))
    path_edges = {frozenset((a, b)) for a, b in zip(path, path[1:])} if path else set()
    drawn = set()
    for u in graph:
        for v in graph[u]:
            e = frozenset((u, v))
            if e in drawn:
                continue
            drawn.add(e)
            (x1, y1), (x2, y2) = pos[u], pos[v]
            on_path = e in path_edges
            ax.plot([x1, x2], [y1, y2], color="tab:red" if on_path else "lightgray", lw=3 if on_path else 1.5, zorder=1)
            if weighted:
                ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(graph[u][v]), fontsize=8, color="tab:red", ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    for v in nodes:
        if node_colors and v in node_colors:
            color, white = node_colors[v], True
        elif order and v in order:
            color, white = plt.cm.viridis(order.index(v) / max(1, len(order) - 1)), True
        else:
            color, white = "#e6e6e6", False
        ax.scatter(*pos[v], s=800, color=color, zorder=2, edgecolor="k", linewidth=0.8)
        txt = str(v) + (f"\n{order.index(v)}" if order and v in order else "")
        ax.text(*pos[v], txt, ha="center", va="center", fontsize=8, color="white" if white else "black", zorder=3)
    ax.set_aspect("equal")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    return close_if_inline(fig)


def draw_grid(grid, visited=None, path=None, title="", size=4.5):
    # grid: list of rows, 1 = wall, 0 = free.
    n, m = len(grid), len(grid[0])
    img = np.array([[1 if grid[r][c] else 0 for c in range(m)] for r in range(n)], dtype=float)
    for r, c in (visited or []):
        if not grid[r][c]:
            img[r][c] = 2
    for r, c in (path or []):
        img[r][c] = 3
    cmap = ListedColormap(["white", "black", "#cfe3ff", "tab:red"])
    fig, ax = plt.subplots(figsize=(size, size))
    ax.imshow(img, cmap=cmap, vmin=0, vmax=3)
    ax.set_xticks(np.arange(-0.5, m, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="#dddddd", lw=0.5)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=10)
    return close_if_inline(fig)


def draw_table(table, row_labels, col_labels, title="", highlight=(), fmt="{}"):
    # A DP table as a heatmap with the numbers written in; highlight is a set of (row, col) cells.
    arr = np.array(table, dtype=float)
    fig, ax = plt.subplots(figsize=(max(3.5, 0.55 * arr.shape[1] + 1), max(2.5, 0.5 * arr.shape[0] + 1)))
    ax.imshow(arr, cmap="Blues", alpha=0.85)
    highlight = set(highlight)
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            cell = (r, c)
            ax.text(c, r, fmt.format(table[r][c]), ha="center", va="center", fontsize=8,
                    color="white" if cell in highlight else "black",
                    bbox=dict(boxstyle="round,pad=0.25", fc="tab:red", ec="none") if cell in highlight else None)
    ax.set_xticks(range(arr.shape[1]))
    ax.set_xticklabels(col_labels)
    ax.set_yticks(range(arr.shape[0]))
    ax.set_yticklabels(row_labels)
    ax.xaxis.tick_top()
    ax.set_title(title, fontsize=10, pad=18)
    return close_if_inline(fig)
