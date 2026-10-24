import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from test import AddSignalSamplesAreEqual, MultiplySignalByConst, SignalSamplesAreEqual
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2

signals = []
signal_names = []
frequency_state = None
frequency_window = None
frequency_figure = None

# ==================== COMMON FUNCTIONS ====================

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

# Subtraction: second selected signal minus first selected signal to match the task reference files
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

# ==================== QUANTIZATION ====================

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

# Quantization table and error graph in a separate window
def show_quantization_details(indices, samples, intervals, encoded, quantized, errors):
    details_window = tk.Toplevel(window)
    details_window.title("Quantization Results")
    details_window.geometry("1150x600")
    details_window.minsize(850, 450)
    main_frame = ttk.Frame(details_window, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    table_frame = ttk.LabelFrame(main_frame, text="Quantization Table", padding=5)
    table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
    columns = ("n", "x", "interval", "encoded", "xq", "error", "error_sq")
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    headings = {"n": "n", "x": "x[n]", "interval": "Interval", "encoded": "Encoded",
                "xq": "xq[n]", "error": "e[n]", "error_sq": "e[n]^2"}
    widths = {"n": 45, "x": 75, "interval": 65, "encoded": 70,
              "xq": 75, "error": 75, "error_sq": 75}
    for column in columns:
        table.heading(column, text=headings[column])
        table.column(column, width=widths[column], anchor="center")
    y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=table.xview)
    table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    table.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")
    x_scroll.grid(row=1, column=0, sticky="ew")
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)
    for i in range(len(samples)):
        table.insert("", tk.END, values=(indices[i], f"{samples[i]:.6g}", intervals[i],
                     encoded[i], f"{quantized[i]:.6g}", f"{errors[i]:.6g}", f"{errors[i] ** 2:.6g}"))

    plot_frame = ttk.LabelFrame(main_frame, text="Quantization Error Graph", padding=5)
    plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    error_figure, error_ax = plt.subplots(figsize=(5, 4))
    error_ax.plot(indices, errors, linewidth=1)
    error_ax.axhline(0, linestyle="--", linewidth=0.8)
    error_ax.set_title("Quantization Error")
    error_ax.set_xlabel("Sample Index (n)")
    error_ax.set_ylabel("Error e[n]")
    error_ax.grid(True)
    error_figure.tight_layout()
    error_canvas = FigureCanvasTkAgg(error_figure, master=plot_frame)
    error_canvas.draw()
    error_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def close_details():
        plt.close(error_figure)
        details_window.destroy()
    details_window.protocol("WM_DELETE_WINDOW", close_details)

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
        interval, encoded, quantized, errors = quantize_signal(signal["indices"], signal["samples"], levels)
    except ValueError:
        messagebox.showerror("Quantization", "Enter a valid number of levels or bits.")
        return
    print("\nQuantization Results")
    print("Interval indices:", interval)
    print("Encoded values:", encoded)
    print("Quantized values:", quantized)
    print("Quantization errors:", errors)
    show_result(signal["indices"], quantized, "Quantized Signal")
    show_quantization_details(signal["indices"], signal["samples"], interval, encoded, quantized, errors)
    return interval, encoded, quantized, errors

# ==================== TASK 3: FREQUENCY DOMAIN ====================

# Manual DFT: do not use numpy.fft or another built-in transform
# X[k] = sum(x[n] * (cos(2*pi*k*n/N) - j*sin(2*pi*k*n/N)))
def calculate_dft(samples):
    count = len(samples)
    spectrum = []
    for k in range(count):
        total = 0j
        for n in range(count):
            angle = 2 * math.pi * k * n / count
            total += samples[n] * complex(math.cos(angle), -math.sin(angle))
        spectrum.append(total)
    return spectrum

# Manual IDFT: x[n] = (1/N) * sum(X[k] * (cos(2*pi*k*n/N) + j*sin(2*pi*k*n/N)))
def calculate_idft(spectrum):
    count = len(spectrum)
    samples = []
    for n in range(count):
        total = 0j
        for k in range(count):
            angle = 2 * math.pi * k * n / count
            total += spectrum[k] * complex(math.cos(angle), math.sin(angle))
        samples.append((total / count).real)
    return samples

# Read frequency-domain test files containing amplitude and phase columns
# The test files may use a trailing "f" after floating-point values.
def read_amplitude_phase_file(file_name):
    amplitudes, phases = [], []
    with open(file_name, "r") as file:
        file.readline()
        file.readline()
        file.readline()
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                amplitudes.append(float(parts[0].rstrip("fF")))
                phases.append(float(parts[1].rstrip("fF")))
    return amplitudes, phases

# Compare arrays using a tolerance because reference files round their values
def compare_test_values(task_name, actual, expected, tolerance=0.001):
    if len(actual) != len(expected):
        print(f"{task_name} Test case failed: different number of values")
        return False
    for i in range(len(actual)):
        if abs(actual[i] - expected[i]) > tolerance:
            print(f"{task_name} Test case failed: value mismatch at position {i}")
            print(f"Expected: {expected[i]}, got: {actual[i]}")
            return False
    print(f"{task_name} Test case passed successfully")
    return True

def compare_test_signal(task_name, actual_indices, actual_samples, file_name, tolerance=0.001):
    expected_indices, expected_samples = read_signal_file(file_name)
    if actual_indices != expected_indices:
        print(f"{task_name} Test case failed: indices do not match")
        return False
    return compare_test_values(task_name, actual_samples, expected_samples, tolerance)

# ==================== TASK 3 TESTS: DFT, IDFT AND REMOVE DC ====================
def run_task3_tests():
    print("\n===== TASK 3 TESTS: DFT / IDFT / REMOVE DC =====")
    try:
        # DFT: compare the calculated magnitude and phase with the reference file
        indices, samples = read_signal_file("resources/Task3/Test Cases/DFT/input_Signal_DFT.txt")
        spectrum = calculate_dft(samples)
        expected_amplitudes, expected_phases = read_amplitude_phase_file(
            "resources/Task3/Test Cases/DFT/Output_Signal_DFT_A,Phase.txt"
        )
        actual_amplitudes = [abs(value) for value in spectrum]
        actual_phases = [0.0 if abs(value) < 1e-12 else math.atan2(value.imag, value.real)
                         for value in spectrum]
        compare_test_values("DFT Amplitude", actual_amplitudes, expected_amplitudes, 0.001)
        compare_test_values("DFT Phase", actual_phases, expected_phases, 0.001)

        # IDFT: convert the reference amplitude/phase pairs back to complex values
        input_amplitudes, input_phases = read_amplitude_phase_file(
            "resources/Task3/Test Cases/IDFT/Input_Signal_IDFT_A,Phase.txt"
        )
        input_spectrum = []
        for i in range(len(input_amplitudes)):
            amplitude = input_amplitudes[i]
            phase = input_phases[i]
            input_spectrum.append(complex(amplitude * math.cos(phase),
                                          amplitude * math.sin(phase)))
        reconstructed_samples = calculate_idft(input_spectrum)
        expected_indices, expected_samples = read_signal_file(
            "resources/Task3/Test Cases/IDFT/Output_Signal_IDFT.txt"
        )
        compare_test_values("IDFT", reconstructed_samples, expected_samples, 0.001)

        # Remove DC: set F(0) to zero and reconstruct the time-domain signal
        dc_indices, dc_samples = read_signal_file(
            "resources/Task3/Remove DC component/DC_component_input.txt"
        )
        dc_spectrum = calculate_dft(dc_samples)
        dc_spectrum[0] = 0j
        dc_result = calculate_idft(dc_spectrum)
        compare_test_signal(
            "Remove DC Component", dc_indices, dc_result,
            "resources/Task3/Remove DC component/DC_component_output.txt", 0.001
        )
    except (OSError, ValueError, IndexError) as error:
        print("Task 3 tests could not be completed:", error)
        print("Make sure the Task 3 files are under resources/Task3/Test Cases and resources/Task3/Remove DC component.")
    print("===== TASK 3 TESTS FINISHED =====")

def get_frequency_data():
    if frequency_state is None:
        return None
    spectrum = frequency_state["spectrum"]
    count = len(spectrum)
    frequencies = [k * frequency_state["sampling_frequency"] / count for k in range(count)]
    magnitudes = [abs(value) for value in spectrum]
    maximum = frequency_state["reference_maximum"]
    if maximum > 0:
        amplitudes = [value / maximum for value in magnitudes]
    else:
        amplitudes = [0.0 for value in magnitudes]
    phases = []
    for value in spectrum:
        if abs(value) < 1e-12:
            phases.append(0.0)
        else:
            phases.append(math.degrees(math.atan2(value.imag, value.real)))
    return frequencies, amplitudes, phases

def close_frequency_window():
    global frequency_window, frequency_figure
    if frequency_figure is not None:
        plt.close(frequency_figure)
        frequency_figure = None
    if frequency_window is not None:
        try:
            if frequency_window.winfo_exists():
                frequency_window.destroy()
        except tk.TclError:
            pass
        frequency_window = None

def show_frequency_domain():
    global frequency_window, frequency_figure
    if frequency_state is None:
        messagebox.showwarning("Frequency Domain", "Calculate the DFT first.")
        return
    values = get_frequency_data()
    if values is None:
        return
    frequencies, amplitudes, phases = values
    close_frequency_window()
    frequency_window = tk.Toplevel(window)
    frequency_window.title("Frequency Domain")
    frequency_window.geometry("900x720")
    frame = ttk.Frame(frequency_window, padding=8)
    frame.pack(fill=tk.BOTH, expand=True)

    frequency_figure, (amp_ax, phase_ax) = plt.subplots(2, 1, figsize=(8, 6))
    amp_ax.plot(frequencies, amplitudes, marker="o", markersize=3)
    amp_ax.set_title("Normalized Amplitude vs Frequency")
    amp_ax.set_xlabel("Frequency (Hz)")
    amp_ax.set_ylabel("Normalized Amplitude")
    amp_ax.set_ylim(0, 1.05)
    amp_ax.grid(True)
    phase_ax.plot(frequencies, phases, marker="o", markersize=3)
    phase_ax.set_title("Phase vs Frequency")
    phase_ax.set_xlabel("Frequency (Hz)")
    phase_ax.set_ylabel("Phase (degrees)")
    phase_ax.grid(True)
    frequency_figure.tight_layout()
    graph_canvas = FigureCanvasTkAgg(frequency_figure, master=frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    dominant = []
    for k, amplitude in enumerate(amplitudes):
        if amplitude > 0.5:
            dominant.append(f"k={k}: {frequencies[k]:.6g} Hz (amplitude={amplitude:.3f})")
    if dominant:
        dominant_text = "\n".join(dominant)
    else:
        dominant_text = "No components have normalized amplitude greater than 0.5."
    label = ttk.Label(frame, text="Dominant frequencies (amplitude > 0.5):\n" + dominant_text,
                      justify=tk.LEFT, wraplength=850)
    label.pack(fill=tk.X, pady=(6, 0))
    frequency_window.protocol("WM_DELETE_WINDOW", close_frequency_window)

def run_dft():
    global frequency_state
    selected = signal_list.curselection()
    if len(selected) != 1:
        messagebox.showwarning("DFT", "Select exactly one signal first.")
        return
    sampling_frequency = simpledialog.askfloat(
        "DFT", "Enter the sampling frequency in Hz:", minvalue=0.000001
    )
    if sampling_frequency is None:
        return
    signal = signals[selected[0]]
    spectrum = calculate_dft(signal["samples"])
    reference_maximum = max((abs(value) for value in spectrum), default=0)
    frequency_state = {
        "indices": signal["indices"][:],
        "samples": signal["samples"][:],
        "source_name": signal_names[selected[0]],
        "sampling_frequency": sampling_frequency,
        "spectrum": spectrum,
        "reference_maximum": reference_maximum
    }
    show_frequency_domain()
    return spectrum

def modify_frequency_component():
    if frequency_state is None:
        messagebox.showwarning("Modify Component", "Calculate the DFT first.")
        return
    spectrum = frequency_state["spectrum"]
    count = len(spectrum)
    k = simpledialog.askinteger("Modify Component", f"Enter component index (0 to {count - 1}):",
                                minvalue=0, maxvalue=count - 1)
    if k is None:
        return
    kind = simpledialog.askstring("Modify Component", "Enter Amplitude or Phase:")
    if kind is None:
        return
    kind = kind.strip().lower()
    mirror = (count - k) % count
    current = spectrum[k]
    magnitude = abs(current)
    current_phase = math.atan2(current.imag, current.real)

    if kind.startswith("a"):
        new_amplitude = simpledialog.askfloat(
            "Modify Amplitude", "Enter normalized amplitude from 0 to 1:", minvalue=0, maxvalue=1
        )
        if new_amplitude is None:
            return
        new_magnitude = new_amplitude * frequency_state["reference_maximum"]
        updated = complex(new_magnitude * math.cos(current_phase),
                          new_magnitude * math.sin(current_phase))
        if mirror == k:
            spectrum[k] = complex(updated.real, 0.0)
        else:
            spectrum[k] = updated
            spectrum[mirror] = updated.conjugate()
    elif kind.startswith("p"):
        new_phase_degrees = simpledialog.askfloat("Modify Phase", "Enter new phase in degrees:")
        if new_phase_degrees is None:
            return
        new_phase = math.radians(new_phase_degrees)
        if mirror == k:
            phase_mod = new_phase_degrees % 360
            if not (math.isclose(phase_mod, 0, abs_tol=1e-7) or math.isclose(phase_mod, 180, abs_tol=1e-7)):
                messagebox.showwarning(
                    "Modify Phase",
                    "This component is its own symmetric counterpart. For a real reconstructed signal, its phase must be 0 or 180 degrees."
                )
                return
            spectrum[k] = complex(magnitude * math.cos(new_phase), 0.0)
        else:
            updated = complex(magnitude * math.cos(new_phase), magnitude * math.sin(new_phase))
            spectrum[k] = updated
            spectrum[mirror] = updated.conjugate()
    else:
        messagebox.showwarning("Modify Component", "Choose Amplitude or Phase.")
        return
    show_frequency_domain()

def remove_dc_component():
    if frequency_state is None:
        messagebox.showwarning("Remove DC", "Calculate the DFT first.")
        return
    frequency_state["spectrum"][0] = 0j
    show_frequency_domain()
    print("DC component F(0) removed.")

def reconstruct_idft():
    if frequency_state is None:
        messagebox.showwarning("IDFT", "Calculate the DFT first.")
        return
    samples = calculate_idft(frequency_state["spectrum"])
    indices = frequency_state["indices"][:]
    name = frequency_state["source_name"] + " IDFT Reconstruction"
    signals.append({"indices": indices, "samples": samples})
    signal_names.append(name)
    signal_list.insert(tk.END, name)
    signal_list.selection_clear(0, tk.END)
    signal_list.selection_set(tk.END)
    display_selected_signals()
    return indices, samples

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
    SignalSamplesAreEqual("Subtraction", "resources/task2/outputs/signal1-signal2.txt", indices, samples)
    indices, samples = subtract_signals([0, 2])
    SignalSamplesAreEqual("Subtraction", "resources/task2/outputs/signal1-signal3.txt", indices, samples)
    indices, samples = square_signal(s1i, s1)
    SignalSamplesAreEqual("Squaring", "resources/task2/outputs/Output squaring signal 1.txt", indices, samples)
    indices, samples = normalize_signal(s1i, s1, "-1 to 1")
    SignalSamplesAreEqual("Normalization", "resources/task2/outputs/normalize of signal 1 (from -1 to 1)-- output.txt", indices, samples)
    indices, samples = normalize_signal(s2i, s2, "0 to 1")
    SignalSamplesAreEqual("Normalization", "resources/task2/outputs/normlize signal 2 (from 0 to 1 )-- output.txt", indices, samples)
    indices, samples = accumulate_signal(s1i, s1)
    SignalSamplesAreEqual("Accumulation", "resources/task2/outputs/output accumulation for signal1.txt", indices, samples)

    print("\n===== QUANTIZATION TESTS =====")
    qi, qs = read_signal_file("resources/task2/inputs/Quan1_input.txt")
    interval, encoded, quantized, errors = quantize_signal(qi, qs, 8)
    QuantizationTest1("resources/task2/outputs/Quan1_Out.txt", encoded, quantized)
    qi, qs = read_signal_file("resources/task2/inputs/Quan2_input.txt")
    interval, encoded, quantized, errors = quantize_signal(qi, qs, 4)
    QuantizationTest2("resources/task2/outputs/Quan2_Out.txt", interval, encoded, quantized, errors)

    # Task 3 DFT, IDFT and Remove DC reference tests
    run_task3_tests()

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

# New menu for the DFT / IDFT task
frequency_menu = tk.Menu(menu_bar, tearoff=0)
frequency_menu.add_command(label="Calculate DFT", command=run_dft)
frequency_menu.add_command(label="Modify Component Amplitude / Phase", command=modify_frequency_component)
frequency_menu.add_command(label="Remove DC Component", command=remove_dc_component)
frequency_menu.add_command(label="Reconstruct Signal (IDFT)", command=reconstruct_idft)
menu_bar.add_cascade(label="Frequency Domain", menu=frequency_menu)

test_menu = tk.Menu(menu_bar, tearoff=0)
test_menu.add_command(label="Run Tests", command=run_tests)
test_menu.add_command(label="Run Task 3 Tests", command=run_task3_tests)
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
