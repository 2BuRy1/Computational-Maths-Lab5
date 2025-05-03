import os
import re

def get_input_method():
    while True:
        method = input("Выберите метод ввода данных (1 – файл, 2 – консоль, 3 - функции на выбор): ").strip()
        if method in {"1", "2", "3"}:
            return method
        print("Ошибка: введите 1, 2 или 3.")

def read_input_from_file():
    while True:
        path = input("Введите путь к файлу: ").strip()
        if not os.path.isfile(path):
            print("Ошибка: файл не найден. Попробуйте снова.")
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Ошибка: не удалось открыть файл ({e}).")
            continue

        x_vals = []
        y_vals = []
        arg = None
        valid = True

        for idx, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            # Проверка строки arg = ...
            match = re.match(r"arg\s*=\s*([-+]?[0-9]*\.?[0-9]+)", line, re.IGNORECASE)
            if match:
                try:
                    arg = float(match.group(1))
                except ValueError:
                    print(f"Строка {idx}: неверное значение аргумента.")
                    valid = False
                    break
                continue

            # Ожидаем строку из двух чисел
            parts = line.split()
            if len(parts) != 2:
                print(f"Строка {idx}: должно быть 2 числа, а не {len(parts)}.")
                valid = False
                break

            try:
                x = float(parts[0].replace(",", "."))
                y = float(parts[1].replace(",", "."))
                x_vals.append(x)
                y_vals.append(y)
            except ValueError:
                print(f"Строка {idx}: неверный формат чисел.")
                valid = False
                break

        if not valid:
            continue

        if len(x_vals) < 2:
            print("Ошибка: нужно минимум 2 точки.")
            continue

        if arg is None:
            print("Ошибка: аргумент (строка вида 'arg = число') не найден в файле.")
            continue

        return x_vals, y_vals, arg