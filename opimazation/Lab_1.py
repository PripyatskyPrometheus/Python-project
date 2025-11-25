from math import exp, sqrt


def dichotomy(f, a, b, epsilon):
    count = 0
    while (b - a) > 2*epsilon:
        # Вычисляем среднюю точку
        x1 = (a + b)/2 - epsilon
        x2 = (a + b)/2 + epsilon
        # Сравниваем значения функции в точках x1 и x2
        if f(x1) < f(x2):
            b = x2
        else:
            a = x1
        count+=2
    return (a + b) / 2, (b - a) / 2, count


def golden_section(f, a, b, epsilon):
    count = 2
    # Коэффициент золотого сечения
    phi = (1 + 5**0.5) / 2
    resphi = 2 - phi  # Это 1/phi

    # Вычисляем начальные точки внутри интервала
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    
    # Считаем значения функции в этих точках
    f_x1 = f(x1)
    f_x2 = f(x2)

    # Основной цикл
    while (b - a) > 2*epsilon:
        if f_x1 < f_x2:
            # Сужаем интервал к x2
            b = x2
            x2 = x1
            f_x2 = f_x1  # Сохраняем уже рассчитанное значение
            x1 = a + resphi * (b - a)
            f_x1 = f(x1)  # Считаем новое значение функции
        else:
            # Сужаем интервал к x1
            a = x1
            x1 = x2
            f_x1 = f_x2  # Сохраняем уже рассчитанное значение
            x2 = b - resphi * (b - a)
            f_x2 = f(x2)  # Считаем новое значение функции
        count+=1

    # Возвращаем среднюю точку и интервал неопределенности
    return (a + b) / 2, (b - a) / 2, count


def fibonachi_numbers(n):
    # Функция для вычисления чисел Фибоначчи до n-го
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def fibonachi(f, a, b, n):
    # Вычисляем последовательность чисел Фибоначчи
    fib_seq = fibonachi_numbers(n)
    # Начальные значения для точек внутри интервала
    x1 = a + (b - a) * (fib_seq[n - 2] / fib_seq[n]) 
    x2 = a + (b - a) * (fib_seq[n - 1] / fib_seq[n])

    # Считаем значения функции в начальных точках
    fx1 = f(x1)
    fx2 = f(x2)

    # Основной цикл
    for i in range(n - 1, 1, -1):
        if fx1 < fx2:
            b = x2
            x2 = x1
            fx2 = fx1  
            x1 = a + (b - a) * (fib_seq[i - 2] / fib_seq[i]) 
            fx1 = f(x1) 
        else:
            a = x1
            x1 = x2
            fx1 = fx2 
            x2 = a + (b - a) * (fib_seq[i - 1] / fib_seq[i])
            fx2 = f(x2)

    minimum = (a + b)/2
    uncertainty = (b - a)/2
    return minimum, uncertainty

if __name__ == '__main__':  
    f = lambda x: 1 - exp(-(x - 2)**2)
    result, uncertainty, iterations = dichotomy(f, -3, 5, 0.0001)
    print(f"Минимум находится на уровне x = {result}, интервал неопределённости = {uncertainty}, количество итераций = {iterations}")

    result, uncertainty, count = golden_section(f, -3, 5, 0.0001)
    print(f"Минимум находится на уровне x = {result}, интервал неопределённости = {uncertainty}, количество итераций = {count}")

    result, uncertainty = fibonachi(f, -3, 5, 24)
    print(f"Минимум находится на уровне x = {result}, интервал неопределённости = {uncertainty}")