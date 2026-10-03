# Signal Processing Framework

Python implementation of Task 1.

## Features

- Load signal samples from `.txt` files.
- Display a signal in continuous representation.
- Display a signal in discrete representation.
- Display multiple signals at the same time.
- Add any number of signals sample-by-sample.
- Multiply a signal by a constant.
- Multiplication by `-1` automatically inverts the signal.

## TXT file format

A TXT file can contain samples separated by:
- spaces
- commas
- tabs
- new lines

Example:

```text
1 2 3 4 5
```

or:

```text
1
2
3
4
5
```

For addition, the selected signals must have the same number of samples.

## Installation

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

Tkinter is normally included with standard Python on Windows.

## Run

```bash
python signal_processing_framework.py
```

## How to use

1. Click **Load TXT Signal**.
2. Select a `.txt` signal file.
3. The signal appears in both continuous and discrete plots.
4. Load another signal if needed.
5. Select multiple signals using Ctrl + Click.
6. Choose **Arithmetic Operations -> Addition** or click **Addition**.
7. For multiplication, select exactly one signal and click **Multiply by Constant**.
8. Enter the constant. Entering `-1` inverts the signal.
