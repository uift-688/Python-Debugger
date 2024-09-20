try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import PathCompleter, Completer, Completion, WordCompleter
    from time import sleep
    from sys import exit as sexit
    import ast
    import importlib
    import traceback
    import sys
    import os
except ModuleNotFoundError:
    print("依存関係を読み込めませんでした。終了します。")
    from sys import sexit
    sexit(1)


# 現在の実行中のファイルのパスを取得
current_file_path = os.path.abspath(sys.argv[0])

class NumberCompleter(Completer):
    def __init__(self, numbers):
        self.numbers = numbers

    def get_completions(self, document, complete_event):
        # 現在の入力内容
        current_input = document.text

        # 数字の補完候補を生成
        for number in self.numbers:
            if str(number).startswith(current_input):
                yield Completion(str(number), start_position=-len(current_input))

yes_no_completer = WordCompleter(['y', 'n'], ignore_case=True)

completer_n = NumberCompleter(list(range(0, 60)))
sec = prompt('再実行するまでの秒数を入力してください(0で一回の実行になります): ', completer=completer_n)
try:    
    sec = float(sec)
except ValueError:
    print("入力した秒数が整数・小数ではありません。終了します。")
    sexit(3)

def output_traceback(e):
    tb = traceback.format_exception(e.__class__, e, e.__traceback__)
    if tb:
        print("".join(tb))  # スタックトレースをそのまま出力
    else:
        print(f"{type(e).__name__}: {e}")


completer = PathCompleter()
def path_select():
    global path
    path = prompt('パスを入力してください: ', completer=completer)

if sec != 0:
    max_retry = prompt('再実行の回数を選択してください。: ', completer=completer_n)

def validate_python_file(path):
    if not path.endswith(".py"):
        select = prompt("このファイルは.pyファイルではないため、実行できない可能性があります(内部がPythonファイルではないならば)。実行しますか？ [Y/n]: ", completer=yes_no_completer)
        if select == 'n':
            print("終了しています...")
            sexit(0)

def get_imported_modules(code):
    tree = ast.parse(code)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imported_modules.add(node.module)
    return imported_modules

major = sys.version_info.major
minor = sys.version_info.minor
micro = sys.version_info.micro

if major < 3 or (major == 3 and minor < 6):
    print("このデバックプログラムの最低限のサポートバージョンは3.6以上です。動作しない可能性があります(推奨バージョン: 3.7)。")
    select = prompt("実行しますか？ [Y/n]: ", completer=yes_no_completer)
    if select == "n":
        sexit(0)

while True:
    path_select()
    validate_python_file(path)
    if not os.path.exists(path):
        print("そのファイルは存在しません。終了します。")
        sexit(3)
    try:
        count = 0
        while True:
            count += 1
            if count > int(max_retry):
                print("最大試行回数を超えました。再試行を停止します。")
                break
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
            except IOError as e:
                print(f"ファイルが読み込めません: {e}")
                select = prompt("別のファイルを開きますか？ [Y/n]: ", completer=yes_no_completer)
                if select == "y":
                    path_select()

            import_modules = get_imported_modules(code)
            import_module_dict = {}

            for name in import_modules:
                if name in list(globals().keys()):
                    import_module_dict[name] = globals()[module]
                try:
                    module = importlib.import_module(name)
                except ModuleNotFoundError as e:
                    print(f"モジュールが存在しません: {name} - {e}")
                    continue
                except Exception as e:
                    print(f"モジュール {name} のインポート中にエラーが発生しました: {e}")
                    continue
                import_module_dict[name] = module

            try:
                compiled_code = compile(code, '<string-Executer>', 'exec')
                exec_globals = {name: getattr(__builtins__, name) for name in dir(__builtins__)}
                exec_globals.update(import_module_dict)
                print(f"{path} を実行中...")
                exec(compiled_code, exec_globals, {})
            except Exception as e:
                print(f"{path}: E: {e}")
                output_traceback(e)

            if sec != 0:
                print(f"{sec}秒後に自動的に再実行されます。")
                sleep(sec)
            elif sec == 0:
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        select = prompt("別のファイルを開きますか？ [Y/n]: ", completer=yes_no_completer)
        if select == "n":
            print("終了しています...")
            sexit(0)
        elif select == "y":
            continue
