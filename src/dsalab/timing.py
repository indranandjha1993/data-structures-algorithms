"""Timing helpers: measure how running time grows with input size."""
import time
import matplotlib.pyplot as plt
from .common import close_if_inline


def time_it(fn, *args, repeats=3, **kwargs):
    # Best of several runs, in seconds. Best-of is less noisy than the mean on a busy laptop.
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(*args, **kwargs)
        best = min(best, time.perf_counter() - t0)
    return best


def growth_plot(funcs, sizes, title="running time vs input size", repeats=3, loglog=True, reference=None):
    # funcs: {label: fn(n)}. sizes: a list, or {label: list} when functions need different ranges.
    # reference: optional {label: fn(n) -> relative cost} curves drawn as dashed guides, scaled to the first point.
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for label, fn in funcs.items():
        ns = sizes[label] if isinstance(sizes, dict) else sizes
        ts = [time_it(fn, n, repeats=repeats) for n in ns]
        ax.plot(ns, ts, "o-", label=label)
        if reference and label in reference:
            ref = reference[label]
            scale = ts[0] / ref(ns[0]) if ref(ns[0]) else 1
            ax.plot(ns, [scale * ref(n) for n in ns], "--", color="gray", lw=1)
    if loglog:
        ax.set_xscale("log")
        ax.set_yscale("log")
    ax.set_xlabel("n (input size)")
    ax.set_ylabel("seconds, best of %d" % repeats)
    ax.set_title(title, fontsize=11)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8)
    fig.tight_layout()
    return close_if_inline(fig)
