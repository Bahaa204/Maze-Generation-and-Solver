# maze_control_gui.py
"""
Maze Control GUI (Tkinter) - runs maze solver (pyamaze) in a separate process so the
pyamaze window (which uses Tkinter) is fully independent from this control UI.

Requirements:
- Place your solver wrappers (AStar, DFS, BFS, Wallfollowing) in the Algorithms/ folder.
- Run this script directly: python maze_control_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from multiprocessing import Process, set_start_method
import sys
import traceback

# For type hints
from typing import Dict


# ---------- Helper: spawn runner executed inside the child process ----------
def _child_runner(module_name: str, func_name: str, params: dict):
    """Run the maze solver in a separate process"""
    import importlib

    try:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        func(**params)
    except Exception:
        print(
            f"Error in child process running {module_name}.{func_name}", file=sys.stderr
        )
        traceback.print_exc()


# ---------- Main GUI ----------
class MazeControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Control Panel")
        self.geometry("820x640")
        self.resizable(False, False)

        # ---------- Color / Style ----------
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        BG = "#23272A"
        PANEL = "#2E3336"
        FG = "#E6EEF3"
        ACCENT = "#2AA198"

        self.configure(bg=BG)
        style.configure("TLabel", background=BG, foreground=FG, font=("Helvetica", 11))
        style.configure(
            "Header.TLabel",
            font=("Helvetica", 16, "bold"),
            foreground=FG,
            background=BG,
        )
        style.configure("TFrame", background=BG)
        style.configure("TRadiobutton", background=BG, foreground=FG)
        style.configure("TCheckbutton", background=BG, foreground=FG)
        style.configure("TButton", font=("Helvetica", 11))

        # ---------- Variables ----------
        self.config_mode = tk.StringVar(value="default")
        self.algorithm = tk.StringVar(value="A*")

        self.rows = tk.IntVar(value=10)
        self.cols = tk.IntVar(value=10)
        self.theme = tk.StringVar(value="dark")
        self.loop_percent = tk.IntVar(value=0)
        self.start_x = tk.IntVar(value=1)
        self.start_y = tk.IntVar(value=1)

        self.shape = tk.StringVar(value="square")
        self.filled = tk.BooleanVar(value=False)
        self.footprints = tk.BooleanVar(value=True)
        self.color = tk.StringVar(value="cyan")

        # Map algorithm names to modules and functions
        self.algo_map: Dict[str, tuple[str, str]] = {
            "A*": ("Algorithms.AStar", "AStar"),
            "DFS": ("Algorithms.DFS", "DFS"),
            "BFS": ("Algorithms.BFS", "BFS"),
            "Wallfollowing": ("Algorithms.WallFollowing", "Wallfollowing"),
        }

        # ---------- Build UI ----------
        self._build_ui(BG, PANEL, FG, ACCENT)
        self._setup_bindings()
        self._apply_constraints()

    # ---------- Bindings ----------
    def _setup_bindings(self):
        self.config_mode.trace_add("write", lambda *a: self._apply_constraints())
        self.algorithm.trace_add("write", lambda *a: self._apply_constraints())
        self.shape.trace_add("write", lambda *a: self._apply_constraints())
        self.rows.trace_add("write", lambda *a: self._update_start_limits())
        self.cols.trace_add("write", lambda *a: self._update_start_limits())

    # ---------- Constraint Updates ----------
    def _apply_constraints(self):
        is_default = self.config_mode.get() == "default"

        maze_widgets = [
            self.rows_spin,
            self.cols_spin,
            self.theme_combo,
            self.loop_spin,
            self.start_x_spin,
            self.start_y_spin,
        ]
        for w in maze_widgets:
            w.config(state="disabled" if is_default else "normal")

        # Shape constraints
        algo = self.algorithm.get()
        if algo == "Wallfollowing":
            self.shape.set("arrow")
            self.shape_combo.config(state="disabled")
        else:
            self.shape_combo.config(state="readonly")

        if self.shape.get() == "arrow":
            self.filled.set(False)
            self.filled_chk.config(state="disabled")
        else:
            self.filled_chk.config(state="normal")

        # Color constraints
        allowed_colors = ["black", "blue", "cyan", "green", "yellow"]
        if algo == "A*":
            allowed_colors.append("red")
        self.color_combo.config(values=allowed_colors)
        if self.color.get() not in allowed_colors:
            self.color.set("cyan")

    def _update_start_limits(self):
        """Ensure start_x and start_y are within rows/cols"""
        rows = self.rows.get()
        cols = self.cols.get()

        self.start_x_spin.configure(from_=1, to=rows)
        if self.start_x.get() > rows:
            self.start_x.set(rows)

        self.start_y_spin.configure(from_=1, to=cols)
        if self.start_y.get() > cols:
            self.start_y.set(cols)

    # ---------- Build UI Widgets ----------
    def _build_ui(self, bg, panel, fg, accent):
        header = ttk.Label(
            self, text="Maze Generator & Solver — Control Panel", style="Header.TLabel"
        )
        header.pack(pady=(12, 8))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=12, pady=6)

        # --- Left Frame: Configuration & Algorithm ---
        left = ttk.Frame(container)
        left.grid(row=0, column=0, sticky="n", padx=(0, 8))

        # Configuration mode
        cfg_frame = ttk.LabelFrame(left, text="Configuration Mode", padding=10)
        cfg_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Radiobutton(
            cfg_frame, text="Default", value="default", variable=self.config_mode
        ).grid(row=0, column=0, padx=8, pady=4, sticky="w")
        ttk.Radiobutton(
            cfg_frame, text="Custom", value="custom", variable=self.config_mode
        ).grid(row=0, column=1, padx=8, pady=4, sticky="w")

        # Algorithm selection
        algo_frame = ttk.LabelFrame(left, text="Solving Algorithm", padding=10)
        algo_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.algo_combo = ttk.Combobox(
            algo_frame,
            values=list(self.algo_map.keys()),
            state="readonly",
            textvariable=self.algorithm,
            width=20,
        )
        self.algo_combo.grid(row=0, column=0, pady=6, padx=6)

        # Agent options
        agent_frame = ttk.LabelFrame(left, text="Agent (Solver) Options", padding=10)
        agent_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(agent_frame, text="Shape:").grid(row=0, column=0, sticky="w")
        self.shape_combo = ttk.Combobox(
            agent_frame,
            values=["square", "arrow"],
            state="readonly",
            textvariable=self.shape,
            width=12,
        )
        self.shape_combo.grid(row=0, column=1, padx=8)
        self.filled_chk = ttk.Checkbutton(
            agent_frame, text="Filled (square only)", variable=self.filled
        )
        self.filled_chk.grid(row=0, column=2, padx=8)
        self.footprints_chk = ttk.Checkbutton(
            agent_frame, text="Footprints", variable=self.footprints
        )
        self.footprints_chk.grid(row=1, column=0, pady=(8, 0), sticky="w")
        ttk.Label(agent_frame, text="Color:").grid(
            row=1, column=1, sticky="w", padx=(6, 0)
        )
        self.color_combo = ttk.Combobox(
            agent_frame,
            values=["black", "blue", "cyan", "green", "red", "yellow"],
            state="readonly",
            textvariable=self.color,
            width=12,
        )
        self.color_combo.grid(row=1, column=2, padx=8)

        # --- Right Frame: Maze Generation Options ---
        right = ttk.Frame(container)
        right.grid(row=0, column=1, sticky="n", padx=(8, 0))
        maze_frame = ttk.LabelFrame(right, text="Maze Generation Options", padding=10)
        maze_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(maze_frame, text="Rows:").grid(row=0, column=0, sticky="w")
        self.rows_spin = ttk.Spinbox(
            maze_frame, from_=1, to=100, textvariable=self.rows, width=6
        )
        self.rows_spin.grid(row=0, column=1, padx=8)

        ttk.Label(maze_frame, text="Columns:").grid(row=1, column=0, sticky="w")
        self.cols_spin = ttk.Spinbox(
            maze_frame, from_=1, to=100, textvariable=self.cols, width=6
        )
        self.cols_spin.grid(row=1, column=1, padx=8)

        ttk.Label(maze_frame, text="Theme:").grid(row=2, column=0, sticky="w")
        self.theme_combo = ttk.Combobox(
            maze_frame,
            values=["dark", "light"],
            state="readonly",
            textvariable=self.theme,
            width=8,
        )
        self.theme_combo.grid(row=2, column=1, padx=8)

        ttk.Label(maze_frame, text="Loop %:").grid(row=3, column=0, sticky="w")
        self.loop_spin = ttk.Spinbox(
            maze_frame, from_=0, to=100, textvariable=self.loop_percent, width=6
        )
        self.loop_spin.grid(row=3, column=1, padx=8)

        ttk.Label(maze_frame, text="Start X:").grid(row=4, column=0, sticky="w")
        self.start_x_spin = ttk.Spinbox(
            maze_frame, from_=1, to=self.rows.get(), textvariable=self.start_x, width=6
        )
        self.start_x_spin.grid(row=4, column=1, padx=8)

        ttk.Label(maze_frame, text="Start Y:").grid(row=5, column=0, sticky="w")
        self.start_y_spin = ttk.Spinbox(
            maze_frame, from_=1, to=self.cols.get(), textvariable=self.start_y, width=6
        )
        self.start_y_spin.grid(row=5, column=1, padx=8)

        # Run Button
        self.run_btn = ttk.Button(
            self, text="Run Maze Solver", command=self._run_solver
        )
        self.run_btn.pack(pady=(12, 8))

    # ---------- Run Solver ----------
    def _run_solver(self):
        algo = self.algorithm.get()
        if algo not in self.algo_map:
            messagebox.showerror("Error", f"Unknown algorithm: {algo}")
            return

        module_name, func_name = self.algo_map[algo]

        # Build parameters dictionary
        params = {
            "rows": self.rows.get(),
            "cols": self.cols.get(),
            "start_cell": (self.start_x.get(), self.start_y.get()),
            "theme": self.theme.get(),
            "loopPercent": self.loop_percent.get(),
            "shape": self.shape.get(),
            "filled": self.filled.get(),
            "footprints": self.footprints.get(),
            "color": self.color.get(),
        }

        # Wallfollowing ignores shape/filled
        if algo == "Wallfollowing":
            params.pop("shape", None)
            params.pop("filled", None)

        # Run in separate process
        p = Process(target=_child_runner, args=(module_name, func_name, params))
        p.start()


def run():
    try:
        set_start_method("spawn")
    except RuntimeError:
        pass
    app = MazeControlApp()
    app.mainloop()

def main() -> None:
    run()


if __name__ == "__main__":
    main()
