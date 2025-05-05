import math


def newton_divided_interp(x, div_diff_table, arg):
    n = len(x)
    result = div_diff_table[0][0]
    product = 1
    for i in range(1, n):
        product *= (arg - x[i - 1])
        result += div_diff_table[i][0] * product
    return result


def divided_differences(x, y):
    n = len(x)
    table = [y.copy()]
    for i in range(1, n):
        row = []
        for j in range(n - i):
            numerator = table[i - 1][j + 1] - table[i - 1][j]
            denominator = x[j + i] - x[j]
            row.append(numerator / denominator)
        table.append(row)
    return table

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

    def gauss_interpolation(x, y, arg):
        n = len(x)
        if n < 2:
            raise ValueError("Need at least 2 points for interpolation")

        h = x[1] - x[0]

        center_idx = n // 2

        fin_diffs = finite_differences(y)

        dts = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5]

        t = (arg - x[center_idx]) / h

        result = y[center_idx]

        for k in range(1, n):
            product = 1
            for j in range(k):
                product *= (t + dts[j])

            base_idx = center_idx - (k // 2)


            if arg <= x[center_idx] and k % 2 == 0:
                diff_idx = base_idx - 1
            else:
                diff_idx = base_idx

            if diff_idx < 0 or diff_idx >= len(fin_diffs[k]):
                break

            delta = fin_diffs[k][diff_idx]
            term = product * delta / math.factorial(k)
            result += term

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

    lagrange_val = lagrange_interpolation(x_sorted, y_sorted, arg)
    new_table = divided_differences(x_sorted, y_sorted)
    newton_val = newton_divided_interp(x_sorted, new_table, arg)
    gauss_val = gauss_interpolation(x_sorted, y_sorted, arg)

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
        "Интерполяция Гаусса": gauss_val,
        "Интерполяция Лагранжа": lagrange_val,
        "diff_table": diff_table,
        "x_sorted": x_sorted,
        "y_sorted": y_sorted,
        "arg": arg
    }






