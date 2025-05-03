import math

def solve(x, y, arg):
    if len(x) != len(y):
        raise ValueError("Количество x и y значений должно совпадать")
    if len(x) < 2:
        raise ValueError("Нужно как минимум 2 точки для интерполяции")

    points = sorted(zip(x, y), key=lambda p: p[0])
    x_sorted = [p[0] for p in points]
    y_sorted = [p[1] for p in points]

    def finite_differences(y):
        n = len(y)
        table = [y.copy()]
        for i in range(1, n):
            row = []
            for j in range(n - i):
                row.append(table[i - 1][j + 1] - table[i - 1][j])
            table.append(row)
        return table

    diff_table = finite_differences(y_sorted)

    def newton_interpolation(x, y, arg, diff_table):
        n = len(x)
        h = x[1] - x[0]

        if arg <= x[n // 2]:
            t = (arg - x[0]) / h
            result = y[0]
            product = 1
            for i in range(1, n):
                product *= (t - (i - 1)) / i
                result += product * diff_table[i][0]
        else:
            t = (arg - x[-1]) / h
            result = y[-1]
            product = 1
            for i in range(1, n):
                product *= (t + (i - 1)) / i
                result += product * diff_table[i][-1]
        return result

    def lagrange_interpolation(x, y, arg):
        n = len(x)
        result = 0.0
        for i in range(n):
            term = y[i]
            for j in range(n):
                if j != i:
                    term *= (arg - x[j]) / (x[i] - x[j])
            result += term
        return result

    newton_val = newton_interpolation(x_sorted, y_sorted, arg, diff_table)
    lagrange_val = lagrange_interpolation(x_sorted, y_sorted, arg)

    def format_diff_table(diff_table):
        max_len = max(len(str(val)) for row in diff_table for val in row)
        formatted = []
        for i, row in enumerate(diff_table):
            formatted_row = [f"{'Δ' * i}y:"] + [f"{val:>{max_len}.4f}" for val in row]
            formatted.append(" ".join(formatted_row))
        return "\n".join(formatted)

    return {
        "Таблица конечных разностей": format_diff_table(diff_table),
        "Интерполяция Ньютона": newton_val,
        "Интерполяция Лагранжа": lagrange_val,
        "diff_table": diff_table,
        "x_sorted": x_sorted,
        "y_sorted": y_sorted
    }

def newton_poly(x_sorted, y_sorted, diff_table, x_dense):
    h = x_sorted[1] - x_sorted[0]
    n = len(x_sorted)
    y_interp = []

    for x in x_dense:
        if x <= x_sorted[n // 2]:
            t = (x - x_sorted[0]) / h
            y = y_sorted[0]
            prod = 1
            for i in range(1, len(diff_table)):
                if len(diff_table[i]) < 1:
                    continue
                prod *= (t - (i - 1)) / i
                y += prod * diff_table[i][0]
        else:
            t = (x - x_sorted[-1]) / h
            y = y_sorted[-1]
            prod = 1
            for i in range(1, len(diff_table)):
                if len(diff_table[i]) < 1:
                    continue
                prod *= (t + (i - 1)) / i
                y += prod * diff_table[i][-1]
        y_interp.append(y)
    return y_interp

def lagrange_poly(x_vals, y_vals, x_dense):
    def L(i, x):
        result = 1
        for j in range(len(x_vals)):
            if j != i:
                result *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        return result

    y_interp = []
    for x in x_dense:
        y = sum(y_vals[i] * L(i, x) for i in range(len(x_vals)))
        y_interp.append(y)
    return y_interp
