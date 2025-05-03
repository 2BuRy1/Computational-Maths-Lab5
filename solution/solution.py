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

    # Интерполяция Ньютона (вперед/назад)
    def newton_interpolation(x, y, arg, diff_table):
        n = len(x)
        h = x[1] - x[0]

        # Выбираем формулу в зависимости от положения arg
        if arg <= x[n // 2]:  # Ближе к началу - вперед
            t = (arg - x[0]) / h
            result = y[0]
            product = 1
            for i in range(1, n):
                product *= (t - (i - 1)) / i
                result += product * diff_table[i][0]
        else:  # Ближе к концу - назад
            t = (arg - x[-1]) / h
            result = y[-1]
            product = 1
            for i in range(1, n):
                product *= (t + (i - 1)) / i
                result += product * diff_table[i][-1]
        return result

    # Интерполяция Лагранжа
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
        "Интерполяция Лагранжа": lagrange_val
    }