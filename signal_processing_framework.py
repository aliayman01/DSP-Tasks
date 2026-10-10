
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from test import AddSignalSamplesAreEqual, MultiplySignalByConst, SignalSamplesAreEqual
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2

signals = []
signal_names = []

# COMMON FUNCTIONS
def read_signal_file(file_name):
    indices, samples = [], []
    with open(file_name, "r") as file:
        file.readline()
        file.readline()
        file.readline()
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                indices.append(int(parts[0]))
                samples.append(float(parts[1]))
    return indices, samples

def show_result(indices, samples, title):
    ax1.clear()
    ax2.clear()
    ax1.plot(indices, samples, marker="o")
    ax2.stem(indices, samples)
    ax1.set_title(title + " - Continuous")
    ax2.set_title(title + " - Discrete")
    ax1.set_xlabel("Index")
    ax2.set_xlabel("Index")
    ax1.set_ylabel("Amplitude")
    ax2.set_ylabel("Amplitude")
    ax1.grid()
    ax2.grid()
    canvas.draw()

def read_signal():
    file_name = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_name:
        return
    try:
        indices, samples = read_signal_file(file_name)
    except (ValueError, OSError) as error:
        messagebox.showerror("File Error", str(error))
        return
    if not samples:
        messagebox.showwarning("Error", "No signal samples found.")
        return
    signals.append({"indices": indices, "samples": samples})
    name = "Signal " + str(len(signals))
    signal_names.append(name)
    signal_list.insert(tk.END, name)
    signal_list.selection_clear(0, tk.END)
    signal_list.selection_set(tk.END)
    display_selected_signals()

def display_selected_signals():
    selected = signal_list.curselection()
    ax1.clear()
    ax2.clear()
    for index in selected:
        indices = signals[index]["indices"]
        samples = signals[index]["samples"]
        ax1.plot(indices, samples, marker="o", label=signal_names[index])
        ax2.stem(indices, samples, label=signal_names[index])
    ax1.set_title("Continuous Representation")
    ax2.set_title("Discrete Representation")
    ax1.set_xlabel("Index")
    ax2.set_xlabel("Index")
    ax1.set_ylabel("Amplitude")
    ax2.set_ylabel("Amplitude")
    ax1.grid()
    ax2.grid()
    if selected:
        ax1.legend()
        ax2.legend()
    canvas.draw()

def clear_signals():
    signals.clear()
    signal_names.clear()
    signal_list.delete(0, tk.END)
    ax1.clear()
    ax2.clear()
    ax1.set_title("Continuous Representation")
    ax2.set_title("Discrete Representation")
    canvas.draw()

# ==================== TASK 1 ====================

# Addition
def add_signals(selected):
    if len(selected) < 2:
        return None, None
    first = signals[selected[0]]
    result_indices = first["indices"]
    for index in selected:
        if signals[index]["indices"] != result_indices:
            return None, None
    result_samples = []
    for i in range(len(first["samples"])):
        total = 0
        for index in selected:
            total += signals[index]["samples"][i]
        result_samples.append(total)
    return result_indices[:], result_samples

def addition():
    selected = signal_list.curselection()
    if len(selected) < 2:
        messagebox.showwarning("Addition", "Select at least two signals.")
        return
    indices, samples = add_signals(selected)
    if indices is None:
        messagebox.showwarning("Addition", "Signals must have matching indices.")
        return
    show_result(indices, samples, "Addition Result")
    return indices, samples

# Multiplication
def multiply_signal(indices, samples, constant):
    result_samples = []
    for sample in samples:
        result_samples.append(sample * constant)
    return indices[:], result_samples

def multiplication():
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("Multiplication", "Select exactly one signal.")
        return
    signal = signals[selected[0]]
    constant = simpledialog.askfloat("Multiplication", "Enter the constant:")
    if constant is None:
        return
    indices, samples = multiply_signal(signal["indices"], signal["samples"], constant)
    show_result(indices, samples, "Multiplication Result")
    return indices, samples

# ==================== TASK 2 ====================

# Subtraction: the expected reference outputs determine the order
def subtract_signals(selected):
    if len(selected) != 2:
        return None, None
    first = signals[selected[0]]
    second = signals[selected[1]]
    if first["indices"] != second["indices"]:
        return None, None
    result_samples = []
    for i in range(len(first["samples"])):
        result_samples.append(second["samples"][i] - first["samples"][i])
    return first["indices"][:], result_samples

def subtraction():
    selected = signal_list.curselection()
    if len(selected) != 2:
        messagebox.showwarning("Subtraction", "Select exactly two signals.")
        return
    indices, samples = subtract_signals(selected)
    if indices is None:
        messagebox.showwarning("Subtraction", "Signals must have matching indices.")
        return
    show_result(indices, samples, "Subtraction Result")
    return indices, samples

# Squaring
def square_signal(indices, samples):
    result_samples = []
    for sample in samples:
        result_samples.append(sample * sample)
    return indices[:], result_samples

def squaring():
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("Squaring", "Select exactly one signal.")
        return
    signal = signals[selected[0]]
    indices, samples = square_signal(signal["indices"], signal["samples"])
    show_result(indices, samples, "Squared Signal")
    return indices, samples

# Normalization
def normalize_signal(indices, samples, mode):
    minimum = min(samples)
    maximum = max(samples)
    result_samples = []
    for sample in samples:
        if maximum == minimum:
            value = 0
        elif mode == "-1 to 1":
            value = 2 * (sample - minimum) / (maximum - minimum) - 1
        else:
            value = (sample - minimum) / (maximum - minimum)
        result_samples.append(value)
    return indices[:], result_samples

def normalization():
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("Normalization", "Select exactly one signal.")
        return
    mode = simpledialog.askstring("Normalization", "Enter -1 to 1 or 0 to 1:")
    if mode not in ("-1 to 1", "0 to 1"):
        if mode is not None:
            messagebox.showwarning("Normalization", "Enter -1 to 1 or 0 to 1.")
        return
    signal = signals[selected[0]]
    indices, samples = normalize_signal(signal["indices"], signal["samples"], mode)
    show_result(indices, samples, "Normalized Signal (" + mode + ")")
    return indices, samples

# Accumulation
def accumulate_signal(indices, samples):
    result_samples = []
    total = 0
    for sample in samples:
        total += sample
        result_samples.append(total)
    return indices[:], result_samples

def accumulation():
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("Accumulation", "Select exactly one signal.")
        return
    signal = signals[selected[0]]
    indices, samples = accumulate_signal(signal["indices"], signal["samples"])
    show_result(indices, samples, "Accumulated Signal")
    return indices, samples

# Quantization
def quantize_signal(indices, samples, levels):
    if levels < 2:
        raise ValueError("The number of levels must be at least 2.")
    minimum = min(samples)
    maximum = max(samples)
    step = (maximum - minimum) / levels
    interval_indices, encoded_values = [], []
    quantized_values, errors = [], []
    bits = (levels - 1).bit_length()

    for sample in samples:
        if step == 0:
            interval = 0
            quantized = sample
        else:
            interval = int((sample - minimum) / step)
            interval = max(0, min(interval, levels - 1))
            quantized = minimum + (interval + 0.5) * step
        interval_indices.append(interval + 1)
        encoded_values.append(format(interval, "0" + str(bits) + "b"))
        quantized_values.append(quantized)
        errors.append(quantized - sample)
    return interval_indices, encoded_values, quantized_values, errors

def quantization():
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("Quantization", "Select exactly one signal.")
        return
    answer = simpledialog.askstring("Quantization", "Enter number of levels or bits (e.g. 4 or 3 bits):")
    if answer is None:
        return
    try:
        if "bit" in answer.lower():
            bits = int(answer.lower().replace("bits", "").replace("bit", "").strip())
            if bits < 1:
                raise ValueError
            levels = 2 ** bits
        else:
            levels = int(answer)
        signal = signals[selected[0]]
        interval, encoded, quantized, errors = quantize_signal(
            signal["indices"], signal["samples"], levels
        )
    except ValueError:
        messagebox.showerror("Quantization", "Enter a valid number of levels or bits.")
        return
    print("\nQuantization Results")
    print("Interval indices:", interval)
    print("Encoded values:", encoded)
    print("Quantized values:", quantized)
    print("Quantization errors:", errors)
    show_result(signal["indices"], quantized, "Quantized Signal")
    return interval, encoded, quantized, errors

# ==================== TESTING ====================

def run_tests():
    print("\n===== TASK 1 TESTS =====")
    s1i, s1 = read_signal_file("resources/task1/inputs/Signal1.txt")
    s2i, s2 = read_signal_file("resources/task1/inputs/Signal2.txt")
    s3i, s3 = read_signal_file("resources/task1/inputs/Signal3.txt")

    old_signals = signals[:]
    signals.clear()
    signals.extend([
        {"indices": s1i, "samples": s1},
        {"indices": s2i, "samples": s2},
        {"indices": s3i, "samples": s3}
    ])

    indices, samples = add_signals([0, 1])
    AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", indices, samples,
        "resources/task1/outputs/Signal1+Signal2.txt")
    indices, samples = add_signals([0, 2])
    AddSignalSamplesAreEqual("Signal1.txt", "Signal3.txt", indices, samples,
        "resources/task1/outputs/Signal1+Signal3.txt")
    indices, samples = multiply_signal(s1i, s1, 5)
    MultiplySignalByConst(5, indices, samples,
        "resources/task1/outputs/MultiplySignalByConstant-Signal1 - by 5.txt")
    indices, samples = multiply_signal(s2i, s2, 10)
    MultiplySignalByConst(10, indices, samples,
        "resources/task1/outputs/MultiplySignalByConstant-Signal2 - by 10.txt")

    print("\n===== TASK 2 TESTS =====")
    indices, samples = subtract_signals([0, 1])
    SignalSamplesAreEqual("Subtraction", "resources/task2/outputs/signal1-signal2.txt",
        indices, samples)
    indices, samples = subtract_signals([0, 2])
    SignalSamplesAreEqual("Subtraction", "resources/task2/outputs/signal1-signal3.txt",
        indices, samples)
    indices, samples = square_signal(s1i, s1)
    SignalSamplesAreEqual("Squaring", "resources/task2/outputs/Output squaring signal 1.txt",
        indices, samples)
    indices, samples = normalize_signal(s1i, s1, "-1 to 1")
    SignalSamplesAreEqual("Normalization",
        "resources/task2/outputs/normalize of signal 1 (from -1 to 1)-- output.txt",
        indices, samples)
    indices, samples = normalize_signal(s2i, s2, "0 to 1")
    SignalSamplesAreEqual("Normalization",
        "resources/task2/outputs/normlize signal 2 (from 0 to 1 )-- output.txt",
        indices, samples)
    indices, samples = accumulate_signal(s1i, s1)
    SignalSamplesAreEqual("Accumulation",
        "resources/task2/outputs/output accumulation for signal1.txt",
        indices, samples)

    print("\n===== QUANTIZATION TESTS =====")
    qi, qs = read_signal_file("resources/task2/inputs/Quan1_input.txt")
    interval, encoded, quantized, errors = quantize_signal(qi, qs, 8)
    QuantizationTest1("resources/task2/outputs/Quan1_Out.txt", encoded, quantized)

    qi, qs = read_signal_file("resources/task2/inputs/Quan2_input.txt")
    interval, encoded, quantized, errors = quantize_signal(qi, qs, 4)
    QuantizationTest2("resources/task2/outputs/Quan2_Out.txt",
        interval, encoded, quantized, errors)

    signals.clear()
    signals.extend(old_signals)
    print("\n===== TESTS FINISHED =====")

# ==================== MAIN PROGRAM ====================

window = tk.Tk()
window.title("Signal Processing Framework")
window.geometry("1200x750")

menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Load Signal", command=read_signal)
file_menu.add_command(label="Clear All Signals", command=clear_signals)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

arithmetic_menu = tk.Menu(menu_bar, tearoff=0)
arithmetic_menu.add_command(label="Addition", command=addition)
arithmetic_menu.add_command(label="Multiplication", command=multiplication)
arithmetic_menu.add_command(label="Subtraction", command=subtraction)
arithmetic_menu.add_command(label="Squaring", command=squaring)
arithmetic_menu.add_command(label="Normalization", command=normalization)
arithmetic_menu.add_command(label="Accumulation", command=accumulation)
arithmetic_menu.add_command(label="Quantization", command=quantization)
menu_bar.add_cascade(label="Arithmetic Operations", menu=arithmetic_menu)

test_menu = tk.Menu(menu_bar, tearoff=0)
test_menu.add_command(label="Run Tests", command=run_tests)
menu_bar.add_cascade(label="Testing", menu=test_menu)
window.config(menu=menu_bar)

tk.Button(window, text="Load Signal", command=read_signal, width=20).pack(pady=4)
tk.Button(window, text="Addition", command=addition, width=20).pack(pady=4)
tk.Button(window, text="Multiplication", command=multiplication, width=20).pack(pady=4)
tk.Button(window, text="Clear All", command=clear_signals, width=20).pack(pady=4)

signal_list = tk.Listbox(window, height=6, width=40, selectmode=tk.EXTENDED)
signal_list.pack(pady=8)
signal_list.bind("<<ListboxSelect>>", lambda event: display_selected_signals())

figure, (ax1, ax2) = plt.subplots(2, 1)
figure.tight_layout(h_pad=3)
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

window.mainloop()
