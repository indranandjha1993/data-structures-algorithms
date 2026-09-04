"""Shared helpers for the dsalab package."""
import os
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import display, clear_output


def is_static(flag=None):
    # Static mode renders plain figures instead of widgets (used for headless execution).
    if flag is not None:
        return bool(flag)
    return os.environ.get("DSALAB_STATIC", "") == "1"


def caption(text):
    print(text)


def close_if_inline(fig):
    # Same convention as Qiskit's plotting functions: close the figure so that returning it
    # from the last line of a cell shows it exactly once.
    if "inline" in matplotlib.get_backend().lower():
        plt.close(fig)
    return fig


def display_static(*figs):
    for f in figs:
        if f is not None:
            display(f)
            plt.close(f)


def show_in(out, *figs):
    with out:
        clear_output(wait=True)
        for f in figs:
            if f is not None:
                display(f)
                plt.close(f)
