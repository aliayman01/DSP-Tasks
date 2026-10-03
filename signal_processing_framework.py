import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Store all signals
signals = []
signal_names = []


# Read a signal from a TXT file
def read_signal():
    file_name = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if file_name == "":
        return

    indices = []
    samples = []

    file = open(file_name, "r")

    # Skip the 3 header lines
    file.readline()
    file.readline()
    file.readline()

    # Read index and sample
    line = file.readline()

    while line:
        parts = line.strip().split()

        if len(parts) >= 2:
            indices.append(int(parts[0]))
            samples.append(float(parts[1]))

        line = file.readline()

    file.close()

    if len(samples) == 0:
        messagebox.showwarning(
            "Error",
            "The file does not contain any signal samples."
        )
        return

    # Store the signal
    signals.append({
        "indices": indices,
        "samples": samples
    })

    name = "Signal " + str(len(signals))
    signal_names.append(name)

    signal_list.insert(tk.END, name)

    # Select the new signal
    signal_list.selection_clear(0, tk.END)
    signal_list.selection_set(tk.END)

    display_selected_signals()


# Display selected signals
def display_selected_signals():
    selected = signal_list.curselection()

    ax1.clear()
    ax2.clear()

    if len(selected) == 0:
        ax1.set_title("Continuous Representation")
        ax2.set_title("Discrete Representation")
        canvas.draw()
        return

    for index in selected:

        indices = signals[index]["indices"]
        samples = signals[index]["samples"]

        # Continuous representation
        ax1.plot(
            indices,
            samples,
            marker="o",
            label=signal_names[index]
        )

        # Discrete representation
        ax2.stem(
            indices,
            samples,
            label=signal_names[index]
        )

    ax1.set_title("Continuous Representation")
    ax2.set_title("Discrete Representation")

    ax1.set_xlabel("Index")
    ax1.set_ylabel("Amplitude")

    ax2.set_xlabel("Index")
    ax2.set_ylabel("Amplitude")

    ax1.grid()
    ax2.grid()

    ax1.legend()
    ax2.legend()

    canvas.draw()


# Add any number of signals
def addition():
    selected = signal_list.curselection()

    if len(selected) < 2:
        messagebox.showwarning(
            "Addition",
            "Please select at least two signals."
        )
        return

    # Check that all signals have the same length
    first_length = len(signals[selected[0]]["samples"])

    for index in selected:

        if len(signals[index]["samples"]) != first_length:
            messagebox.showwarning(
                "Addition Error",
                "All signals must have the same number of samples."
            )
            return

    # Use the indices of the first signal
    result_indices = signals[selected[0]]["indices"]

    result_samples = []

    # Add corresponding samples
    for i in range(first_length):

        total = 0

        for index in selected:
            total = total + signals[index]["samples"][i]

        result_samples.append(total)

    display_result(
        result_indices,
        result_samples,
        "Addition Result"
    )


# Multiply a signal by a constant
def multiplication():
    selected = signal_list.curselection()

    if len(selected) != 1:
        messagebox.showwarning(
            "Multiplication",
            "Please select exactly one signal."
        )
        return

    index = selected[0]

    indices = signals[index]["indices"]
    samples = signals[index]["samples"]

    # Ask for the constant
    constant = simpledialog.askfloat(
        "Multiplication",
        "Enter the constant:"
    )

    if constant is None:
        return

    result_samples = []

    # Multiply every sample
    for i in range(len(samples)):
        result_samples.append(
            samples[i] * constant
        )

    display_result(
        indices,
        result_samples,
        "Multiplication Result"
    )


# Display an arithmetic result
def display_result(indices, samples, title):

    ax1.clear()
    ax2.clear()

    ax1.plot(
        indices,
        samples,
        marker="o"
    )

    ax2.stem(
        indices,
        samples
    )

    ax1.set_title(title + " - Continuous")
    ax2.set_title(title + " - Discrete")

    ax1.set_xlabel("Index")
    ax1.set_ylabel("Amplitude")

    ax2.set_xlabel("Index")
    ax2.set_ylabel("Amplitude")

    ax1.grid()
    ax2.grid()

    canvas.draw()


# Clear all signals
def clear_signals():

    signals.clear()
    signal_names.clear()

    signal_list.delete(0, tk.END)

    ax1.clear()
    ax2.clear()

    ax1.set_title("Continuous Representation")
    ax2.set_title("Discrete Representation")

    canvas.draw()


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("Signal Processing Framework")
window.geometry("1200x750")


# ============================================================
# MENU
# ============================================================

menu_bar = tk.Menu(window)

# File menu
file_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

file_menu.add_command(
    label="Load Signal",
    command=read_signal
)

file_menu.add_command(
    label="Clear All Signals",
    command=clear_signals
)

file_menu.add_separator()

file_menu.add_command(
    label="Exit",
    command=window.destroy
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)


# Arithmetic Operations menu
arithmetic_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

arithmetic_menu.add_command(
    label="Addition",
    command=addition
)

arithmetic_menu.add_command(
    label="Multiplication",
    command=multiplication
)

menu_bar.add_cascade(
    label="Arithmetic Operations",
    menu=arithmetic_menu
)

window.config(menu=menu_bar)


# ============================================================
# BUTTONS
# ============================================================

load_button = tk.Button(
    window,
    text="Load Signal",
    command=read_signal,
    width=20
)

load_button.pack(pady=5)


addition_button = tk.Button(
    window,
    text="Addition",
    command=addition,
    width=20
)

addition_button.pack(pady=5)


multiplication_button = tk.Button(
    window,
    text="Multiplication",
    command=multiplication,
    width=20
)

multiplication_button.pack(pady=5)


clear_button = tk.Button(
    window,
    text="Clear All",
    command=clear_signals,
    width=20
)

clear_button.pack(pady=5)


# ============================================================
# SIGNAL LIST
# ============================================================

# EXTENDED allows selecting multiple signals
signal_list = tk.Listbox(
    window,
    height=8,
    width=40,
    selectmode=tk.EXTENDED
)

signal_list.pack(pady=10)


# Update the graphs when the selection changes
signal_list.bind(
    "<<ListboxSelect>>",
    lambda event: display_selected_signals()
)


# ============================================================
# GRAPHS
# ============================================================

figure, (ax1, ax2) = plt.subplots(2, 1)

figure.tight_layout(
    h_pad=3
)

canvas = FigureCanvasTkAgg(
    figure,
    master=window
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# Start the program
window.mainloop()