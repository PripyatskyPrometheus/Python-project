import numpy as np
import matplotlib.pyplot as plt

from lab_2 import bayes_classifier_for_two_matrix, plot_quadratic_boundary

def experimental_probability_error(X1, X2, w, wn):
    errors_0 = 0 
    errors_1 = 0 
    
    for i in range(X1.shape[1]):
        x = X1[:, i].reshape(-1, 1)
        
        if w.T @ x + wn > 0:
            errors_0 += 1
    
    for i in range(X2.shape[1]):
        x = X2[:, i].reshape(-1, 1)
        
        if w.T @ x + wn < 0: 
            errors_1 += 1
    
    p0 = errors_0 / X1.shape[1]
    p1 = errors_1 / X2.shape[1]
    print(f"Ошибка первого рода: {p0}")
    print(f"Ошибка второго рода: {p1}")

def show_two_borders(sample1, sample2, x0, y0, x1, y1, label):
    plt.scatter(sample1[0], sample1[1], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0], sample2[1], label='Класс Ω1', color='red')

    plt.plot(x0, y0, color='green', label=label)
    plt.plot(x1, y1, color='black', label='Граница Байеса')

    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def part_1_equal_cov(sample1, sample2, M1, M2, B):
    all_data = np.hstack([sample1, sample2])
    min_x, max_x = np.min(all_data[0, :]), np.max(all_data[0, :])

    x = np.linspace(min_x, max_x, 200)
    
    M_diff = M2 - M1
    B_inv = np.linalg.inv(B)

    w = B_inv @ M_diff 
    wn =  -0.5 * M_diff.T @ B_inv @ (M2 + M1)

    y = (-w[0, 0] * x - wn[0, 0]) / w[1, 0]

    print("Ошибки для классификатора Фишера(c одинаковыми В):")
    experimental_probability_error(sample1, sample2, w, wn)

    return x, y

def part_1_unequal_cov(sample_1, sample_2, M1, M2, B1, B2):
    all_data = np.hstack([sample_1, sample_2])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])
    y_min, y_max = np.min(all_data[1, :]), np.max(all_data[1, :])

    x = np.linspace(x_min, x_max, 200)

    M_diff = M2 - M1
    B_inv_edit = np.linalg.inv((B1 + B2) / 2)

    w = B_inv_edit @ M_diff
    sigma_1 = w.T @ B1 @ w
    sigma_2 = w.T @ B2 @ w
    wn = -(1/(sigma_1 + sigma_2)) @ M_diff.T @ B_inv_edit @ ((sigma_1 * M1) + (sigma_2 * M2))
    y = (-w[0, 0] * x - wn[0, 0]) / w[1, 0]

    print("Ошибки для классификатора Фишера(c разными В):")
    experimental_probability_error(sample_1, sample_2, w, wn)

    _ , ax = plt.subplots(figsize=(14, 12))
    ax.scatter(sample_1[0, :], sample_1[1, :], label='Класс Ω0', color='blue')
    ax.scatter(sample_2[0, :], sample_2[1, :], label='Класс Ω1', color='red')

    plot_quadratic_boundary(M1, M2, B1, B2, ax, 'green', 'Граница Байеса', (x_min, x_max), (y_min, y_max), 0.5, 0.5)
    ax.plot(x, y, color='black', label='Граница Фишера')

    ax.legend()
    ax.grid(True)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    plt.show()

    return x, y

def part_2_equal_cov(sample1, sample2):
    all_data = np.hstack([sample1, sample2])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])

    x = np.linspace(x_min, x_max, 200)

    n1 = sample1.shape[1]
    n2 = sample2.shape[1]
    
    sample1_ext = np.vstack([-sample1, -np.ones(n1)])
    sample2_ext = np.vstack([sample2, np.ones(n2)]) 
    
    U = np.hstack([sample1_ext, sample2_ext]).T
    
    Y = np.hstack([np.ones(n1), np.ones(n2)]).reshape(-1, 1)
    U_T = U.T

    W = np.linalg.inv(U_T @ U) @ U_T @ Y

    y = (-W[0, 0] * x - W[2, 0]) / W[1, 0]

    print("Ошибки для классификатора минимизации СКО:")
    experimental_probability_error(sample1, sample2, W[:2], W[2, 0])
    return x, y

def show_three_borders(sample1, sample2, x_sko, y_sko, x_fisher, y_fisher, x_bayes, y_bayes):
    plt.scatter(sample1[0], sample1[1], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0], sample2[1], label='Класс Ω1', color='red')

    plt.plot(x_fisher, y_fisher, color='green', label='Граница Фишера')
    plt.plot(x_bayes, y_bayes, color='black', label='Граница Байеса')
    plt.plot(x_sko, y_sko, color='orange', label='Граница классификатора мин. СКО')

    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def part_2_unequal_cov(sample_1, sample_2, M1, M2, B1, B2, x_fisher, y_fisher):
    all_data = np.hstack([sample_1, sample_2])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])
    y_min, y_max = np.min(all_data[1, :]), np.max(all_data[1, :])
    
    x = np.linspace(x_min, x_max, 200)

    n1 = sample_1.shape[1]
    n2 = sample_2.shape[1]

    sample1_ext = np.vstack([-sample_1, -np.ones(n1)])
    sample2_ext = np.vstack([sample_2, np.ones(n2)]) 
    
    U = np.hstack([sample1_ext, sample2_ext]).T
    
    Y = np.hstack([np.ones(n1), np.ones(n2)]).reshape(-1, 1)
    U_T = U.T

    W = np.linalg.inv(U_T @ U) @ U_T @ Y

    y = (-W[0, 0] * x - W[2, 0]) / W[1, 0]

    print("Ошибки для классификатора минимизации СКО (разные B):")
    experimental_probability_error(sample_1, sample_2, W[:2], W[2, 0])

    _ , ax = plt.subplots(figsize=(14, 12))
    ax.scatter(sample_1[0, :], sample_1[1, :], label='Класс Ω0', color='blue')
    ax.scatter(sample_2[0, :], sample_2[1, :], label='Класс Ω1', color='red')

    plot_quadratic_boundary(M1, M2, B1, B2, ax, 'green', 'Граница Байеса', (x_min, x_max), (y_min, y_max), 0.5, 0.5)
    ax.plot(x_fisher, y_fisher, color='orange', label='Граница Фишера')
    ax.plot(x, y, color='black', label='Граница классфикатора мин. СКО')

    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')
    plt.show()

def show_borders(w_history, x, sample1, sample2):
    plt.figure(figsize=(12, 8))
    plt.scatter(sample1[0, :], sample1[1, :], label='Класс Ω0', color='blue')
    plt.scatter(sample2[0, :], sample2[1, :], label='Класс Ω1', color='red')

    all_data = np.hstack([sample_1, sample_2])
    y_min, y_max = np.min(all_data[1, :]), np.max(all_data[1, :])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])

    W_start = w_history[0]
    if abs(W_start[1, 0]) < 1e-10:
        if abs(W_start[0, 0]) > 1e-10:
            x_vertical = -W_start[2, 0] / W_start[0, 0]
            plt.plot([x_vertical, x_vertical], [y_min, y_max], 'gray', linewidth=2, label='Начальная граница')
    else:
        y_start = (-W_start[0, 0] * x - W_start[2, 0]) / W_start[1, 0]
        plt.plot(x, y_start, 'gray', linewidth=2, label='Начальная граница')
    
    for i in range(0, len(w_history)):
        W = w_history[i]
        if abs(W[1, 0]) < 1e-10:
            if abs(W[0, 0]) > 1e-10:
                x_vertical = -W[2, 0] / W[0, 0]
                plt.plot([x_vertical, x_vertical], [y_min, y_max], 'green', linewidth=0.5)
        else:
            y = (-W[0, 0] * x - W[2, 0]) / W[1, 0]
            plt.plot(x, y, 'green', linewidth=0.5)
    
    W_final = w_history[-1]
    y_final = (-W_final[0, 0] * x - W_final[2, 0]) / W_final[1, 0]
    plt.plot(x, y_final, 'black', linewidth=3, label='Конец')
    
    plt.xlabel('Признак X')
    plt.ylabel('Признак Y')
    plt.title(f'Все {len(w_history)} итераций')
    plt.legend()
    plt.grid(True)
    #plt.axis('equal')
    plt.xlim( x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.show()

def compute_convergence_metrics(w_current, w_prev, X, r):
    cos_angle = np.dot(w_current.flatten(), w_prev.flatten()) / (np.linalg.norm(w_current) * np.linalg.norm(w_prev))
    
    preds = w_current.T @ X
    J_value = np.mean(np.abs(r - preds.flatten()))
    
    weight_change = np.linalg.norm(w_current - w_prev)
    
    return cos_angle, J_value, weight_change

def part_3_equal_cov(sample1, sample2):
    all_data = np.hstack([sample1, sample2])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])
    x = np.linspace(x_min, x_max, 200)

    n1 = sample_1.shape[1]
    n2 = sample_2.shape[1]

    sample1_ext = np.vstack([sample1, np.ones(n1)])
    sample2_ext = np.vstack([sample2, np.ones(n2)]) 

    beta=0.9

    x_s = np.hstack([sample1_ext, sample2_ext])
    r = np.hstack([-np.ones(n1), np.ones(n2)])
    
    w = np.array([[1.0], [-1.0], [0.0]])
    w_history = [w.copy()]

    index = np.arange(n1 + n2)
    counter = 0
    
    convergence_epoch = None
    prev_w = w.copy()
    convergence_threshold = 1 - 1e-5 # 0.99999

    epochs = 50
    for epoch in range(epochs):
        np.random.shuffle(index)
        prev_w = w.copy()

        for k in range(len(index)):
            idx = index[k]
            x_k = x_s[:, idx:idx+1]
            r_k = r[idx]
            
            d = (w.T @ x_k)[0, 0]
            sgn = np.sign(r_k - d)
            
            counter += 1
            alpha = 1.0 / np.power(counter, beta)
            
            w = w + alpha * x_k * sgn
            w_history.append(w.copy())

        cos_angle, J_value, weight_change = compute_convergence_metrics(w, prev_w, x_s, r)
        
        print(f"Эпоха {epoch + 1}: J(W) = {J_value}, cos(θ) = {cos_angle}, ΔW = {weight_change}")
        
        if cos_angle > convergence_threshold and convergence_epoch is None:
            convergence_epoch = epoch + 1
            print(f"Сходимость достигнута на эпохе {convergence_epoch}")
            break
        
        w_history.append(w.copy())

    cos_angle_final, J_final, weight_change_final = compute_convergence_metrics(w, w_history[0], x_s, r)
    
    print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Сходимость достигнута: {'Да' if convergence_epoch else 'Нет'}")
    if convergence_epoch:
        print(f"Эпоха сходимости: {convergence_epoch}")
    print(f"Финальное J(W): {J_final}")
    print(f"Финальное cos(θ): {cos_angle_final}")
    print(f"Финальное ΔW: {weight_change_final}")
    print(f"Финальные веса: [{w[0,0]}, {w[1,0]}, {w[2,0]}]")

    print("Ошибки для классификатора Роббинсона-Монро:")
    experimental_probability_error(sample1, sample2, w[:2], w[2, 0])

    y = (-w[0, 0] * x - w[2, 0]) / w[1, 0]
    show_borders(w_history, x, sample1, sample2)
    
    return x, y

def part_3_unequal_cov(sample_1, sample_2, M1, M2, B1, B2):
    x_rm, y_rm = part_3_equal_cov(sample_1, sample_2)

    all_data = np.hstack([sample_1, sample_2])
    x_min, x_max = np.min(all_data[0, :]), np.max(all_data[0, :])
    y_min, y_max = np.min(all_data[1, :]), np.max(all_data[1, :])
    
    _ , ax = plt.subplots(figsize=(14, 12))
    ax.scatter(sample_1[0, :], sample_1[1, :], label='Класс Ω0', color='blue')
    ax.scatter(sample_2[0, :], sample_2[1, :], label='Класс Ω1', color='red')

    plot_quadratic_boundary(M1, M2, B1, B2, ax, 'green', 'Граница Байеса', (x_min, x_max), (y_min, y_max), 0.5, 0.5)
    ax.plot(x_rm, y_rm, color='black', label='Граница классфикатора Роббинса_Монро')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    M1 = np.array([[0], [0]])
    M2 = np.array([[-1], [1]])
    M3 = np.array([[-1], [-1]])

    B1 = np.array([[0.6, 0.5], [0.5, 0.7]])
    B2 = np.array([[0.4, 0.3], [0.3, 0.5]])
    B3 = np.array([[ 0.3, -0.3], [-0.3, 0.4]])

    sample1 = np.load("MOiRO/class1_normal_equal_cov.npy")
    sample2 = np.load("MOiRO/class2_normal_equal_cov.npy")

    sample_1 = np.load("MOiRO/class1_normal_unequal_cov.npy")
    sample_2 = np.load("MOiRO/class2_normal_unequal_cov.npy")

    if sample1 is None or sample2 is None or sample_1 is None or sample_2 is None:
        print("Ошибка! Файл не найден")

    print(f"Размер первой выборки c одинаковыми B:{sample1.shape}")
    print(f"Размер первой выборки c одинаковыми B:{sample2.shape}\n")

    print(f"Размер первой выборки c разными B:{sample_1.shape}")
    print(f"Размер первой выборки c разными B:{sample_2.shape}\n")

    x_bayes, y_bayes = bayes_classifier_for_two_matrix(sample1, sample2, M1, M2, B1)

    # Пунк 1
    x_fisher, y_fisher = part_1_equal_cov(sample1, sample2, M1, M2, B1)
    label = 'Граница Фишера'
    show_two_borders(sample1, sample2, x_fisher, y_fisher, x_bayes, y_bayes, label)
    x_fisher_un, y_fisher_un = part_1_unequal_cov(sample_1, sample_2, M1, M2, B1, B2)

    # Пункт 2
    x_sko, y_sko = part_2_equal_cov(sample1, sample2)
    show_three_borders(sample1, sample2, x_sko, y_sko, x_fisher, y_fisher, x_bayes, y_bayes)
    part_2_unequal_cov(sample_1, sample_2, M1, M2, B1, B2, x_fisher_un, y_fisher_un)

    #Пункт 3
    x, y = part_3_equal_cov(sample1, sample2)
    label = 'Граница Роббинса-Монро'
    show_two_borders(sample1, sample2, x, y, x_bayes, y_bayes, label)
    part_3_unequal_cov(sample_1, sample_2, M1, M2, B1, B2)