"""Regenerate transit_ai/engine.py from the notebook.

The notebook is the source of truth. Run this after editing it:

    python tools/build_engine.py

Every code cell from SETUP 3 (LLM client) through E4 (outputs) is copied in order. Colab-only cells are left out:
package install, the local Ollama server, the Gradio dashboard and launch, Google Drive, and the Results summary.
IPython display calls are routed to a no-op shim so the module runs outside Jupyter.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "Transit_Agentic_AI_Submission_v5_with_evaluation.ipynb"
OUT = ROOT / "transit_ai" / "engine.py"

SKIP_TITLES = ("SETUP 1", "SETUP 2", "E5 ·", "Results summary")

HEADER = '''# ruff: noqa
# fmt: off
"""GENERATED FILE: do not edit by hand. Edit the notebook, then run `python tools/build_engine.py`.

Engine for the Streamlit app: every non-UI code cell of
notebooks/Transit_Agentic_AI_Submission_v5_with_evaluation.ipynb, in notebook order.
"""
import os as _os
import matplotlib as _matplotlib
_matplotlib.use("Agg")                     # no screen on a server: figures render off-screen
_os.environ.setdefault("MPLBACKEND", "Agg")
from transit_ai._ipython_shim import display, HTML, Markdown, clear_output  # noqa: F401
'''

FOOTER = '''

# ---- end of notebook cells ----
import matplotlib.pyplot as _plt
_plt.close("all")                          # free figures drawn during setup
'''


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    parts, used = [HEADER], []
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        title = src.split("\n", 1)[0].replace("#@title", "").strip()
        if any(t in title for t in SKIP_TITLES):
            continue
        lines = []
        for line in src.split("\n"):
            if re.match(r"\s*[!%]", line):            # shell or magic line
                line = re.sub(r"^(\s*).*$", r"\1pass  # (notebook-only line removed)", line)
            line = line.replace("from IPython.display import", "from transit_ai._ipython_shim import")
            lines.append(line)
        parts.append(f"\n\n# {'=' * 100}\n# notebook cell {i}: {title}\n# {'=' * 100}\n" + "\n".join(lines))
        used.append(i)
    parts.append(FOOTER)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} from {len(used)} notebook cells ({used[0]}..{used[-1]}).")


if __name__ == "__main__":
    main()
