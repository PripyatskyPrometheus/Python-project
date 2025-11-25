import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib.lines import Line2D

def dist_mahalanobis(M1, M2, B):
    M = M1 - M2
    B_inv = np.linalg.inv(B)
    return np.dot(np.dot(M.T, B_inv), M)

def analize_probability_error(M1, M2, B):
    distance = dist_mahalanobis(M1, M2, B)
    print(f"Расстояние Махаланобиса: {distance}")
    
    p_0 = scipy.stats.norm.cdf(-0.5 * np.sqrt(distance))
    p_1 = 1 - scipy.stats.norm.cdf(0.5 * np.sqrt(distance))
    
    print("\nАналитические вероятности ошибок:")
    print(f"Ошибка первого рода p0: {p_0}")
    print(f"Ошибка второго рода p1: {p_1}")
    print(f"Суммарная вероятность ошибочной классификации: {p_0 + p_1}")


def experimental_probability_error(X1, X2, M1, M2, B1, B2, P1=0.5, P2=0.5):
    B1_inv = np.linalg.inv(B1)
    B2_inv = np.linalg.inv(B2)
    
    errors_0 = 0 
    errors_1 = 0 
    
    for i in range(X1.shape[1]):
        x = X1[:, i].reshape(-1, 1)
        d1 = np.log(P1) - np.log(np.linalg.det(B1)) - 0.5 * (x - M1).T @ B1_inv @ (x - M1)
        d2 = np.log(P2) - np.log(np.linalg.det(B2)) - 0.5 * (x - M2).T @ B2_inv @ (x - M2)
        
        if d2 > d1:
            errors_0 += 1
    
    for i in range(X2.shape[1]):
        x = X2[:, i].reshape(-1, 1)
        
        d1 = np.log(P1) - np.log(np.linalg.det(B1)) - 0.5 * (x - M1).T @ B1_inv @ (x - M1)
        d2 = np.log(P2) - np.log(np.linalg.det(B2)) - 0.5 * (x - M2).T @ B2_inv @ (x - M2)
        
        if d1 > d2: 
            errors_1 += 1
    
    p_0 = errors_0 / X1.shape[1]  
    p_1 = errors_1 / X2.shape[1]
    p_total = p_0 + p_1

    return  p_0, p_1, p_total


def bayes_classifier_for_two_matrix(sample1, sample2, M1, M2, B):
    #print("Строим Байсовский классфикатор для двух выборок с одинковыми ковариационными матрицами:\n")

    #print(f"Размер первой выборки:{sample1.shape}")
    #print(f"Размер первой выборки:{sample2.shape}\n")

    min_x = min(np.min(sample1[0, :]), np.min(sample2[0, :]))
    max_x = max(np.max(sample1[0, :]), np.max(sample2[0, :]))
    
    x = np.linspace(min_x, max_x, 100)
    
    B_inv = np.linalg.inv(B)
    M_diff = M1 - M2
    w = M_diff.T @ B_inv
    w0 = -0.5 * (M2 + M1).T @ B_inv @ M_diff

    y = (-w[0, 0] * x - w0[0, 0]) / w[0, 1]

    #plt.scatter(sample1[0], sample1[1], label='Класс Ω0', color='blue')
    #plt.scatter(sample2[0], sample2[1], label='Класс Ω1', color='red')

    #plt.plot(x, y, color='black', label='Байесовская граница')

    #plt.xlabel('Признак X')
    #plt.ylabel('Признак Y')
    #plt.title('Байесовский классификатор для равных ковариационных матриц\n(Случай равных априорных вероятностей)')
    #plt.legend()
    #plt.grid(True)
    #plt.axis('equal')
    #plt.show()

    #analize_probability_error(M1, M2, B)

    #p_0_experimental, p_1_experimental, p_total_experimental = experimental_probability_error(sample1, sample2, M1, M2, B, B, 0.5, 0.5)
    
    #print(f"\nЭкспериментальные вероятности ошибок:")
    #print(f"Ошибка первого рода: {p_0_experimental}")
    #print(f"Ошибка второго рода: {p_1_experimental}")
    #print(f"Суммарная вероятность: {p_total_experimental}")
    
    return x, y

def minimax_classifier(sample1, sample2, M1, M2, B):
    print("Строим минимаксный классфикатор для двух выборок с одинковыми ковариационными матрицами:\n")

    min_x = min(np.min(sample1[0, :]), np.min(sample2[0, :]))
    max_x = max(np.max(sample1[0, :]), np.max(sample2[0, :]))
    
    x = np.linspace(min_x, max_x, 100)

    M_diff = M1 - M2
    B_inv = np.linalg.inv(B)
    w = M_diff.T @ B_inv
    w0 = -0.5 * (M2 + M1).T @ B_inv @ M_diff
    
    y = (-w[0, 0] * x - w0[0, 0]) / w[0, 1]

    plt.scatter(sample1[0], sample1[1], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0], sample2[1], label='Класс Ω1', color='red')

    plt.plot(x, y, color='black', label='Минимаксная граница')

    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.title('Минимаксный классификатор для равных ковариационных матриц')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    #plt.show()

    return x, y

def experemental_fail(sample1, w, w0):
    N = sample1.shape[1]
    errors_01 = 0
    
    for i in range(N):
        x = sample1[:, i].reshape(-1, 1)
        d = w @ x + w0
        
        if d < 0:
            errors_01 += 1
    
    p0_experimental = errors_01 / sample1.shape[1]

    print(f"Экспериментальная p0 = {p0_experimental} ")


def neyman_pearson_classifier(sample1, sample2, M1, M2, B, p0_star=0.05):
    print("Строим классфикатор Неймана-Пирса для двух выборок с одинковыми ковариационными матрицами:\n")

    print(f"Размер первой выборки:{sample1.shape}")
    print(f"Размер первой выборки:{sample2.shape}\n")

    min_x = min(np.min(sample1[0, :]), np.min(sample2[0, :]))
    max_x = max(np.max(sample1[0, :]), np.max(sample2[0, :]))

    x = np.linspace(min_x, max_x, 100)

    M_diff = M1 - M2
    B_inv = np.linalg.inv(B)
    w = M_diff.T @ B_inv
    distance = dist_mahalanobis(M1, M2, B)
    lambda_tilda = scipy.stats.norm.ppf(1 - p0_star) * np.sqrt(distance) - 0.5 * distance
    
    w0 = -0.5 * (M2 + M1).T @ B_inv @ M_diff + lambda_tilda

    y = (-w[0, 0] * x - w0[0, 0]) / w[0, 1]

    experemental_fail(sample1, w, w0)

    plt.scatter(sample1[0], sample1[1], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0], sample2[1], label='Класс Ω1', color='red')

    plt.plot(x, y, color='black', label='Граница Неймана-Пирса')

    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.title('Неймана-Пирса классификатор для равных ковариационных матриц')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

    return x, y

def quadratic_boundary_equation(x1, x2, M1, M2, B1, B2, P1, P2):
    x = np.array([x1, x2]).reshape(-1, 1)
    
    B1_inv = np.linalg.inv(B1)
    B2_inv = np.linalg.inv(B2)
    
    a = 0.5 * x.T @ (B2_inv - B1_inv) @ x
    
    b = (M1.T @ B1_inv - M2.T @ B2_inv) @ x
    
    c = (0.5 * M2.T @ B2_inv @ M2 - 0.5 * M1.T @ B1_inv @ M1 + 0.5 * np.log(np.linalg.det(B2) / np.linalg.det(B1)) + 
        np.log(P1 / P2))
    
    return (a + b + c)[0, 0]

def plot_quadratic_boundary(M1, M2, B1, B2, ax, color, label, x_lim, y_lim, P1, P2):

    x = np.linspace(x_lim[0], x_lim[1], 200)
    y = np.linspace(y_lim[0], y_lim[1], 200)
    X, Y = np.meshgrid(x, y)
    
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = quadratic_boundary_equation(X[i, j], Y[i, j], M1, M2, B1, B2, P1, P2)
    
    contour = ax.contour(X, Y, Z, levels=[0], colors=color, linewidths=2)
    
    legend_line = Line2D([0], [0], color=color, linewidth=2, label=label)
    ax.add_artist(legend_line)
    
    return contour

def error_estimation(p_x, N):
    return np.sqrt((1 - p_x) / (N * p_x))

def get_volume_sample(p, err):
    return (1 - p) / (err**2 * p)

def bayes_classifier_three_classes_unequal_cov(sample1, sample2, sample3, M1, M2, M3, B1, B2, B3, P1=1/3, P2=1/3, P3=1/3):
    print("\nБайесовский классификатор для трех классов с неравными ковариационными матрицами\n")

    all_data = np.hstack([sample1, sample2, sample3])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])
    y_min, y_max = np.min(all_data[1, :]), np.max(all_data[1, :])
    
    _ , ax = plt.subplots(figsize=(14, 12))
    
    ax.scatter(sample1[0, :], sample1[1, :], label='Класс Ω0', color='blue')
    ax.scatter(sample2[0, :], sample2[1, :], label='Класс Ω1', color='red')
    ax.scatter(sample3[0, :], sample3[1, :], label='Класс Ω2', color='black')
    
    plot_quadratic_boundary(M1, M2, B1, B2, ax, 'green', 'Граница Ω0-Ω1', (x_min, x_max), (y_min, y_max), P1, P2)
    plot_quadratic_boundary(M1, M3, B1, B3, ax, 'orange', 'Граница Ω0-Ω2', (x_min, x_max), (y_min, y_max), P1, P3)
    plot_quadratic_boundary(M2, M3, B2, B3, ax, 'brown', 'Граница Ω1-Ω2', (x_min, x_max), (y_min, y_max), P2, P3)
    
    ax.set_xlabel('Признак X')
    ax.set_ylabel('Признак Y')
    ax.set_title('Байесовский классификатор для трех классов\nс неравными ковариационными матрицами')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    plt.show()

    p01, p10, _ = experimental_probability_error(sample1, sample2, M1, M2, B1, B2, P1, P2)

    print(f"Экспериментальные вероятности ошибочной классификации:")
    print(f"Вероятность ошибки первго рода: {p01:}")
    print(f"Вероятность ошибки второго рода: {p10}\n")

    E_01 = error_estimation(p01, sample1.shape[1])
    E_10 = error_estimation(p10, sample2.shape[1])

    print(f"Относительные погрешности:")
    print(f"Для ошибки первго рода: {E_01}")
    print(f"Для ошибки второго рода: {E_10}\n")

    V_0 = np.ceil(get_volume_sample(p01, 0.05))
    V_1 = np.ceil(get_volume_sample(p10, 0.05))
    
    print(f"Объем выборки для погрешности <= 5%:")
    print(f"Для ошибки первго рода: {V_0}")
    print(f"Для ошибки второго рода: {V_1}")

def show_all_borders(sample1, sample2, x_bayes, y_bayes, x_minimax, y_minimax, x_neyman, y_neyman):

    plt.figure(figsize=(12, 8))
    plt.scatter(sample1[0, :], sample1[1, :], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0, :], sample2[1, :], label='Класс Ω1', color='red')

    plt.plot(x_bayes, y_bayes, color='green', label='Байсевская граница')
    plt.plot(x_minimax, y_minimax, color='orange', label='Минимаксная граница')
    plt.plot(x_neyman, y_neyman, color='brown', label='Неймана-Пирса граница')

    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.title('Сравнение всех трёх границ')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def main():
    M1 = np.array([[0], [0]])
    M2 = np.array([[-1], [1]])
    M3 = np.array([[-1], [-1]])

    B1 = np.array([[0.6, 0.5], [0.5, 0.7]])
    B2 = np.array([[0.4, 0.3], [0.3, 0.5]])
    B3 = np.array([[ 0.3, -0.3], [-0.3, 0.4]])

    sample1 = np.load("MOiRO/class1_normal_equal_cov.npy")
    sample2 = np.load("MOiRO/class2_normal_equal_cov.npy")

    if sample1 is None or sample2 is None:
        print("Ошибка! Файл не найден")

    x_bayes, y_bayes = bayes_classifier_for_two_matrix(sample1, sample2, M1, M2, B1)

    x_minimax, y_minimax = minimax_classifier(sample1, sample2, M1, M2, B1)
    x_neyman, y_neyman = neyman_pearson_classifier(sample1, sample2, M1, M2, B1)

    sample_1 = np.load("MOiRO/class1_normal_unequal_cov.npy")
    sample_2 = np.load("MOiRO/class2_normal_unequal_cov.npy")
    sample_3 = np.load("MOiRO/class3_normal_unequal_cov.npy")

    if sample_1 is None or sample_2 is None or sample_3 is None:
        print("Ошибка! Файл не найден")

    bayes_classifier_three_classes_unequal_cov(sample_1, sample_2, sample_3, M1, M2, M3, B1, B2, B3)

    show_all_borders(sample1, sample2, x_bayes, y_bayes, x_minimax, y_minimax, x_neyman, y_neyman)

if __name__ == "__main__":
    main()