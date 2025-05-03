import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from solution.solution import solve, newton_poly, lagrange_poly

x_values = []
y_values = []
entries_x = []
entries_y = []
column_sets = 1
MAX_COLUMN_SETS = 5

FUNCTIONS = {
    "Линейная": lambda x: 2 * x + 3,
    "Квадратичная": lambda x: x ** 2 - 2 * x + 1,
    "Синус": lambda x: math.sin(x),
    "Экспонента": lambda x: math.exp(x),
}

def plot_function(x_vals, y_vals, result, arg, master_frame, func_name=None):
    for w in master_frame.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True)
    ax.set_title("Графики: функция, интерполяции и узлы")

    ax.scatter(x_vals, y_vals, color='black', label='Узлы интерполяции')

    x_dense = [x_vals[0] + i * (x_vals[-1] - x_vals[0]) / 500 for i in range(501)]

    y_interp = newton_poly(result['x_sorted'], result['y_sorted'], result['diff_table'], x_dense)
    y_lagr = lagrange_poly(result['x_sorted'], result['y_sorted'], x_dense)

    ax.plot(x_dense, y_interp, label='Полином Ньютона', color='red', linewidth=2)
    ax.plot(x_dense, y_lagr, label='Полином Лагранжа', color='green', linestyle='--', linewidth=2)

    if func_name and func_name in FUNCTIONS:
        f = FUNCTIONS[func_name]
        y_true = [f(x) for x in x_dense]
        ax.plot(x_dense, y_true, label='Исходная функция', color='blue')

    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    NavigationToolbar2Tk(canvas, master_frame)

def add_column_set():
    global column_sets, entries_x, entries_y

    if column_sets >= MAX_COLUMN_SETS:
        messagebox.showinfo("Информация", f"Достигнуто максимальное количество наборов ({MAX_COLUMN_SETS})")
        return

    col_offset = (column_sets - 1) * 3

    tk.Label(frame_table_input, text=f"Набор {column_sets}").grid(row=0, column=1 + col_offset, columnspan=2)
    tk.Label(frame_table_input, text="X", font=('Arial', 10, 'bold')).grid(row=1, column=1 + col_offset)
    tk.Label(frame_table_input, text="Y", font=('Arial', 10, 'bold')).grid(row=1, column=2 + col_offset)

    for i in range(2, 13):
        point_num = i - 1 + (column_sets - 1) * 11
        tk.Label(frame_table_input, text=f"{point_num}").grid(row=i, column=0 + col_offset)

        entry_x = tk.Entry(frame_table_input, width=10)
        entry_x.grid(row=i, column=1 + col_offset)
        entries_x.append(entry_x)

        entry_y = tk.Entry(frame_table_input, width=10)
        entry_y.grid(row=i, column=2 + col_offset)
        entries_y.append(entry_y)

    column_sets += 1

    if column_sets < MAX_COLUMN_SETS:
        add_column_button.grid(row=0, column=0 + (column_sets - 1) * 3, sticky='w')
    else:
        add_column_button.grid_forget()

def show_table_input():
    frame_function_input.pack_forget()
    frame_table_input.pack()

    global column_sets, entries_x, entries_y, add_column_button, arg_entry
    entries_x.clear()
    entries_y.clear()
    column_sets = 1

    for widget in frame_table_input.winfo_children():
        widget.destroy()

    add_column_button = tk.Button(frame_table_input, text="+", command=add_column_set, width=3)
    add_column_button.grid(row=0, column=0, padx=5, pady=2, sticky='w')
    add_column_set()

    tk.Label(frame_table_input, text="Аргумент:").grid(row=14, column=0, padx=5, pady=5)
    arg_entry = tk.Entry(frame_table_input, width=10)
    arg_entry.grid(row=14, column=1, padx=5, pady=5)

def show_function_input():
    frame_table_input.pack_forget()
    frame_function_input.pack()

    global func_combobox, start_entry, end_entry, points_entry, arg_entry

    for widget in frame_function_input.winfo_children():
        widget.destroy()

    tk.Label(frame_function_input, text="Функция:").grid(row=0, column=0)
    func_combobox = ttk.Combobox(frame_function_input, values=list(FUNCTIONS.keys()), state="readonly")
    func_combobox.grid(row=0, column=1)

    tk.Label(frame_function_input, text="Начало интервала:").grid(row=1, column=0)
    start_entry = tk.Entry(frame_function_input, width=10)
    start_entry.grid(row=1, column=1)

    tk.Label(frame_function_input, text="Конец интервала:").grid(row=2, column=0)
    end_entry = tk.Entry(frame_function_input, width=10)
    end_entry.grid(row=2, column=1)

    tk.Label(frame_function_input, text="Количество точек:").grid(row=3, column=0)
    points_entry = tk.Entry(frame_function_input, width=10)
    points_entry.grid(row=3, column=1)

    tk.Label(frame_function_input, text="Аргумент:").grid(row=4, column=0)
    arg_entry = tk.Entry(frame_function_input, width=10)
    arg_entry.grid(row=4, column=1)

def get_input_data():
    global x_values, y_values
    x_values = []
    y_values = []

    try:
        arg = float(arg_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректное значение аргумента")
        return None, None, None

    if input_mode.get() == "table":
        for i in range(len(entries_x)):
            x_entry = entries_x[i].get()
            y_entry = entries_y[i].get()
            if x_entry and y_entry:
                try:
                    x = float(x_entry.replace(",", "."))
                    y = float(y_entry.replace(",", "."))
                    x_values.append(x)
                    y_values.append(y)
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректные значения в строке {i + 1}")
                    return None, None, None

        if len(x_values) < 2:
            messagebox.showerror("Ошибка", "Нужно минимум 2 точки")
            return None, None, None

    elif input_mode.get() == "function":
        func_name = func_combobox.get()
        if func_name not in FUNCTIONS:
            messagebox.showerror("Ошибка", "Выберите функцию")
            return None, None, None

        try:
            start = float(start_entry.get())
            end = float(end_entry.get())
            num = int(points_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные параметры интервала")
            return None, None, None

        if start >= end or num < 2:
            messagebox.showerror("Ошибка", "Неверный интервал или количество точек")
            return None, None, None

        step = (end - start) / (num - 1)
        func = FUNCTIONS[func_name]
        x_values = [start + i * step for i in range(num)]
        y_values = [func(x) for x in x_values]

    return x_values, y_values, arg


def get_frame_plot():
    return frame_plot

def get_input_mode():
    return input_mode

def get_func_combobox():
    return func_combobox

def setData():
    data = get_input_data()
    if data[0] is None:
        return
    x_vals, y_vals, arg = data
    result = solve(x_vals, y_vals, arg)
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", result['Таблица конечных разностей'] + "\n")
    result_text.insert(tk.END, f"Результаты интерполяции:\nНьютон({arg}) = {result['Интерполяция Ньютона']}\nЛагранж({arg}) = {result['Интерполяция Лагранжа']}\n")

    func_name = func_combobox.get() if input_mode.get() == "function" else None
    plot_function(x_vals, y_vals, result, arg, frame_plot, func_name)

def start():
    global root, input_frame, frame_plot, result_text, add_column_button
    global func_combobox, start_entry, end_entry, points_entry, arg_entry, input_mode
    global frame_table_input, frame_function_input

    root = tk.Tk()
    root.title("Интерполяция")
    root.geometry("1000x700")

    input_mode = tk.StringVar(value="table")

    mode_frame = tk.Frame(root)
    mode_frame.pack(pady=10)
    tk.Radiobutton(mode_frame, text="Табличный ввод", variable=input_mode, value="table", command=show_table_input).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(mode_frame, text="Функция", variable=input_mode, value="function", command=show_function_input).pack(side=tk.LEFT, padx=5)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=5)

    frame_table_input = tk.Frame(input_frame)
    frame_table_input.pack()
    frame_function_input = tk.Frame(input_frame)

    func_combobox = ttk.Combobox(frame_function_input, values=list(FUNCTIONS.keys()), state="readonly")
    start_entry = tk.Entry(frame_function_input, width=10)
    end_entry = tk.Entry(frame_function_input, width=10)
    points_entry = tk.Entry(frame_function_input, width=10)

    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=10)

    solve_button = tk.Button(frame_controls, text="Построить график", command=setData)
    solve_button.pack()

    result_text = tk.Text(frame_controls, height=10, width=80, wrap="word")
    result_text.pack()

    frame_plot = tk.Frame(root)
    frame_plot.pack(pady=5, fill="both", expand=True)

    show_table_input()
    root.mainloop()