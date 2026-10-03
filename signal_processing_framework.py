import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SignalProcessingFramework(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Signal Processing Framework")
        self.geometry("1250x760")
        self.minsize(1050, 650)

        # Stored signals:
        # {name: {"samples": np.ndarray, "source": str}}
        self.signals = {}
        self.signal_counter = 0

        self._build_menu()
        self._build_ui()

    # ------------------------- UI -------------------------

    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Signal from TXT", command=self.load_signal)
        file_menu.add_command(label="Clear All Signals", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        arithmetic_menu = tk.Menu(menubar, tearoff=0)
        arithmetic_menu.add_command(label="Addition", command=self.add_signals)
        arithmetic_menu.add_command(label="Multiplication", command=self.multiply_signal)
        menubar.add_cascade(label="Arithmetic Operations", menu=arithmetic_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _build_ui(self):
        top = tk.Frame(self, padx=10, pady=8)
        top.pack(fill=tk.X)

        tk.Label(
            top,
            text="Signal Processing Framework",
            font=("Arial", 20, "bold")
        ).pack(side=tk.LEFT)

        tk.Button(
            top, text="Load TXT Signal", command=self.load_signal,
            width=16, height=2
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            top, text="Clear All", command=self.clear_all,
            width=12, height=2
        ).pack(side=tk.RIGHT, padx=4)

        # Left control panel
        left = tk.Frame(self, width=300, padx=10, pady=5)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        tk.Label(left, text="Loaded Signals", font=("Arial", 13, "bold")).pack(
            anchor="w", pady=(0, 5)
        )

        list_frame = tk.Frame(left)
        list_frame.pack(fill=tk.BOTH, expand=False)

        self.signal_list = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            height=13,
            exportselection=False
        )
        self.signal_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.signal_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.signal_list.config(yscrollcommand=scrollbar.set)

        self.signal_list.bind("<<ListboxSelect>>", self.on_selection_change)

        tk.Label(
            left,
            text="Select 1 signal for multiplication\nor 2+ signals for addition.",
            justify=tk.LEFT,
            fg="gray"
        ).pack(anchor="w", pady=8)

        tk.Button(
            left, text="Addition", command=self.add_signals,
            height=2
        ).pack(fill=tk.X, pady=3)

        tk.Button(
            left, text="Multiply by Constant", command=self.multiply_signal,
            height=2
        ).pack(fill=tk.X, pady=3)

        tk.Button(
            left, text="Plot Selected Signal(s)", command=self.plot_selected,
            height=2
        ).pack(fill=tk.X, pady=3)

        self.status = tk.StringVar(value="Load a TXT file to begin.")
        tk.Label(
            left, textvariable=self.status, wraplength=270,
            justify=tk.LEFT, fg="navy"
        ).pack(anchor="w", pady=12)

        tk.Label(left, text="Signal data format", font=("Arial", 11, "bold")).pack(
            anchor="w", pady=(15, 4)
        )
        tk.Label(
            left,
            text="TXT files may contain samples separated by spaces, commas, "
                 "or new lines.\n\nExample:\n1 2 3 4 5 3 2 1",
            justify=tk.LEFT,
            fg="gray"
        ).pack(anchor="w")

        # Plot area
        right = tk.Frame(self, padx=5, pady=5)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure, self.axes = plt.subplots(2, 1, figsize=(8, 7))
        self.figure.subplots_adjust(hspace=0.45, left=0.08, right=0.97,
                                    top=0.94, bottom=0.08)

        self.canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self._show_empty_plots()

    # ------------------------- File handling -------------------------

    def load_signal(self):
        filepath = filedialog.askopenfilename(
            title="Select Signal TXT File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filepath:
            return

        try:
            samples = self.read_txt_signal(filepath)

            if samples.size == 0:
                raise ValueError("The selected file contains no numeric samples.")

            self.signal_counter += 1
            base_name = Path(filepath).stem
            name = base_name

            # Avoid duplicate names.
            if name in self.signals:
                name = f"{base_name}_{self.signal_counter}"

            self.signals[name] = {
                "samples": samples,
                "source": filepath
            }

            self.signal_list.insert(tk.END, name)
            self.status.set(
                f"Loaded '{name}' successfully.\n"
                f"Samples: {len(samples)}"
            )

            # Automatically display the newly loaded signal.
            self.signal_list.selection_clear(0, tk.END)
            self.signal_list.selection_set(tk.END)
            self.plot_selected()

        except Exception as exc:
            messagebox.showerror("Error Loading Signal", str(exc))

    @staticmethod
    def read_txt_signal(filepath):
        # Accept spaces, commas, tabs, and newlines.
        text = Path(filepath).read_text(encoding="utf-8")
        text = text.replace(",", " ").replace(";", " ")
        values = np.fromstring(text, sep=" ")

        if values.size == 0:
            # Fallback for files with unusual whitespace.
            tokens = text.split()
            values = np.array([float(x) for x in tokens], dtype=float)

        return values

    # ------------------------- Plotting -------------------------

    def _show_empty_plots(self):
        for ax in self.axes:
            ax.clear()
            ax.grid(True, alpha=0.25)

        self.axes[0].set_title("Continuous Representation")
        self.axes[0].set_xlabel("Sample Index")
        self.axes[0].set_ylabel("Amplitude")

        self.axes[1].set_title("Discrete Representation")
        self.axes[1].set_xlabel("Sample Index")
        self.axes[1].set_ylabel("Amplitude")

        self.canvas.draw()

    def plot_selected(self):
        indices = self.signal_list.curselection()

        if not indices:
            messagebox.showinfo("No Selection", "Select at least one signal.")
            return

        selected = [
            self.signal_list.get(i)
            for i in indices
        ]

        self.plot_names(selected)

    def plot_names(self, names):
        for ax in self.axes:
            ax.clear()
            ax.grid(True, alpha=0.25)

        for name in names:
            samples = self.signals[name]["samples"]
            n = np.arange(len(samples))

            self.axes[0].plot(
                n, samples, marker="o", linewidth=1.5, markersize=3,
                label=name
            )

            self.axes[1].stem(
                n, samples, linefmt="-", markerfmt="o",
                basefmt=" ", label=name
            )

        self.axes[0].set_title("Continuous Representation")
        self.axes[0].set_xlabel("Sample Index")
        self.axes[0].set_ylabel("Amplitude")
        self.axes[0].legend(loc="best")

        self.axes[1].set_title("Discrete Representation")
        self.axes[1].set_xlabel("Sample Index")
        self.axes[1].set_ylabel("Amplitude")
        self.axes[1].legend(loc="best")

        self.figure.tight_layout()
        self.canvas.draw()

        self.status.set(
            "Displaying: " + ", ".join(names)
        )

    # ------------------------- Arithmetic -------------------------

    def add_signals(self):
        indices = self.signal_list.curselection()

        if len(indices) < 2:
            messagebox.showwarning(
                "Addition",
                "Select at least two signals for addition."
            )
            return

        names = [self.signal_list.get(i) for i in indices]
        arrays = [self.signals[name]["samples"] for name in names]

        lengths = [len(arr) for arr in arrays]
        if len(set(lengths)) != 1:
            messagebox.showerror(
                "Addition Error",
                "All signals must contain the same number of samples "
                "for sample-by-sample addition.\n\n"
                f"Selected lengths: {lengths}"
            )
            return

        result = np.sum(arrays, axis=0)

        result_name = self._unique_result_name(
            "Addition(" + " + ".join(names) + ")"
        )
        self.signals[result_name] = {
            "samples": result,
            "source": "Generated by addition"
        }

        self.signal_list.insert(tk.END, result_name)

        self.signal_list.selection_clear(0, tk.END)
        self.signal_list.selection_set(tk.END)

        self.plot_names([result_name])

        self.status.set(
            f"Created {result_name}\n"
            f"Number of samples: {len(result)}"
        )

    def multiply_signal(self):
        indices = self.signal_list.curselection()

        if len(indices) != 1:
            messagebox.showwarning(
                "Multiplication",
                "Select exactly one signal for multiplication."
            )
            return

        name = self.signal_list.get(indices[0])

        constant = simpledialog.askfloat(
            "Multiplication",
            f"Enter a constant to multiply '{name}' by:",
            parent=self
        )

        if constant is None:
            return

        result = self.signals[name]["samples"] * constant

        result_name = self._unique_result_name(
            f"{name} x {constant:g}"
        )
        self.signals[result_name] = {
            "samples": result,
            "source": f"Generated by multiplying {name} by {constant:g}"
        }

        self.signal_list.insert(tk.END, result_name)

        self.signal_list.selection_clear(0, tk.END)
        self.signal_list.selection_set(tk.END)

        self.plot_names([result_name])

        extra = ""
        if constant == -1:
            extra = "\nThe signal was inverted."

        self.status.set(
            f"Created {result_name}\n"
            f"Constant: {constant:g}{extra}"
        )

    # ------------------------- Helpers -------------------------

    def _unique_result_name(self, base):
        name = base
        counter = 2

        while name in self.signals:
            name = f"{base} #{counter}"
            counter += 1

        return name

    def on_selection_change(self, _event=None):
        selected = self.signal_list.curselection()
        if selected:
            names = [self.signal_list.get(i) for i in selected]
            self.status.set("Selected: " + ", ".join(names))

    def clear_all(self):
        if not self.signals:
            return

        answer = messagebox.askyesno(
            "Clear All",
            "Remove all loaded and generated signals?"
        )
        if not answer:
            return

        self.signals.clear()
        self.signal_list.delete(0, tk.END)
        self._show_empty_plots()
        self.status.set("All signals cleared.")

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Signal Processing Framework\n\n"
            "Features:\n"
            "• Read signals from TXT files\n"
            "• Continuous representation\n"
            "• Discrete representation\n"
            "• Addition of multiple signals\n"
            "• Multiplication by a constant\n"
            "• Display multiple signals at the same time"
        )


if __name__ == "__main__":
    app = SignalProcessingFramework()
    app.mainloop()
