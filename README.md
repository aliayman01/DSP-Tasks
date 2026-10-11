# Signal Processing Framework

A Python-based signal processing framework developed for DSP lab tasks. The project loads discrete signals from text files, displays continuous-style and discrete representations, performs signal operations, and compares calculated results against instructor-provided reference outputs.

## Features

### Task 1 — Basic Operations
- Load signal samples from `.txt` files.
- Display one or more signals in continuous-style and discrete (stem) representations.
- Add two or more signals sample by sample.
- Multiply a signal by a constant to amplify or reduce its amplitude.
- Invert a signal by multiplying it by `-1`.

### Task 2 — Additional Operations
- Subtract two signals.
- Square every sample in a signal.
- Normalize samples to either `[0, 1]` or `[-1, 1]`.
- Accumulate a signal using a running sum.
- Quantize samples using a specified number of levels or bits.
- Calculate quantization interval indices, binary encodings, quantized values, and quantization errors.

## Technologies
- Python
- Tkinter for the desktop interface
- Matplotlib for plotting

## Project Structure

```text
DSP-Tasks/
├── signal_processing_framework.py
├── test.py
├── QuanTest1.py
├── QuanTest2.py
├── requirements.txt
└── resources/
    ├── task1/
    │   ├── inputs/
    │   └── outputs/
    └── task2/
        ├── inputs/
        └── outputs/
```

The `resources` folders contain the signal input files and expected outputs used by the tests. Keep the folder names and reference filenames unchanged because the testing code uses these paths.

## Installation

1. Install Python 3.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

On Windows, Tkinter is usually included with the standard Python installation.

## Run the Application

Run this command from the project root:

```bash
python signal_processing_framework.py
```

## Using the Framework

1. Load a signal from a `.txt` file.
2. Select the signal or signals needed for an operation.
3. Choose an operation from **Arithmetic Operations**.
4. For multiplication, enter the constant. Use `-1` to invert the signal.
5. For normalization, enter `-1 to 1` or `0 to 1`.
6. For quantization, enter the number of levels or a bit count, such as `4` levels or `3 bits`.
7. Choose **Testing → Run Tests** to run the included reference comparisons. Results appear in the terminal or PyCharm Run console.

## Signal File Format

The provided signal files contain three header lines followed by rows with an index and sample value. For example:

```text
0
0
1001
0 1000
1 1001
2 1002
```

The reader skips the first three lines, then reads each remaining data row as:

```text
index sample
```

Addition and subtraction require the signals' indices to match.

## Testing

The project uses instructor-provided comparison functions in `test.py`, `QuanTest1.py`, and `QuanTest2.py`. They compare calculated arrays with expected output files under `resources/task1/outputs/` and `resources/task2/outputs/`.

Run the application and choose **Testing → Run Tests**. A passing message for each case indicates that the calculated values match the supplied reference output within the test's tolerance.

## Notes

- Run the program from the project root so paths to `resources/` resolve correctly.
- Keep all input files, expected outputs, and testing scripts in their original locations.
- The continuous-style plots connect sample points for visualization; the discrete plots show individual samples.
