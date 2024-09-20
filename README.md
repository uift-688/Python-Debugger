# Python Script Executor

This is a Python script executor that allows users to select and run Python scripts. It also provides options for automatically re-running the script after a specified time interval, with customizable retries and enhanced error handling.

## Features

- **File Path Auto-Completion**: Helps users easily select Python scripts using `prompt_toolkit`.
- **Module Import Handling**: Automatically detects and imports necessary modules from the script.
- **Error Handling**: Includes detailed traceback for errors encountered during execution.
- **Customizable Re-Runs**: Option to re-run the script after a user-defined time interval or a set number of retries.
- **Support for Python 3.6+**: Ensures compatibility with Python 3.6 and above.

## Requirements

- Python 3.6 or higher
- The following Python packages are required:
  - `prompt_toolkit`
  - `time`
  - `sys`
  - `ast`
  - `importlib`
  - `traceback`
  - `os`

You can install the dependencies by running:

```bash
pip install prompt_toolkit
```

## Usage

1. Download Debugger:

```bash
wget https://raw.githubusercontent.com/uift-688/Python-Debbger/main/Debagger.py
```

2. Run the script:

```bash
python Debbger.py
```

3. Follow the on-screen prompts to select a Python file and execute it. You can also set a time interval for re-running the script and specify the number of retries.

### Example:

```PythonConsole
再実行するまでの秒数を入力してください(0で一回の実行になります): 10
再実行の回数を選択してください。: 5
パスを入力してください: Program.py
Program.py を実行中...
10秒後に自動的に再実行されます。
```

## Error Handling

If an error occurs during script execution, a detailed traceback will be displayed. You can also choose to load a different script or stop the execution.

## Contributions

Feel free to contribute by creating pull requests or submitting issues. Any improvements or bug fixes are appreciated!
