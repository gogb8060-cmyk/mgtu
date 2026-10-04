"""
Лабораторная работа №1. Эмпирический анализ временной сложности.
Вариант: 24 | Параметр: N = 4
"""

import random
import matplotlib.pyplot as plt
import openpyxl
from usage_time import get_usage_time  # Файл должен лежать рядом!

# =============================================================================
# 1. Алгоритмы (Вариант 24)
# =============================================================================
def f2_sum(v):
    """f2: Сумма элементов. Сложность O(n)"""
    return sum(v)

def f4_horner(v, x=2.0):
    """f4: Полином Горнера. Сложность O(n)"""
    if not v:
        return 0.0
    res = v[-1]
    for val in reversed(v[:-1]):
        res = val + x * res
    return res

def f5_max(v):
    """f5: Поиск максимума. Сложность O(n)"""
    return max(v)

def f8_harmonic(v):
    """f8: Среднее гармоническое. Сложность O(n)"""
    n = len(v)
    sum_inv = sum(1.0 / val for val in v)
    return n / sum_inv if sum_inv != 0 else 0.0

def mat_mult_naive(A, B, n):
    """Наивное умножение матриц. Сложность O(n^3)"""
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

# =============================================================================
# 2. Настройка замеров
# =============================================================================
measure = get_usage_time(number=5, ndigits=6)
m_f2 = measure(f2_sum)
m_f4 = measure(f4_horner)
m_f5 = measure(f5_max)
m_f8 = measure(f8_harmonic)
m_mat = get_usage_time(number=3, ndigits=6)(mat_mult_naive)

# =============================================================================
# 3. Параметры эксперимента
# =============================================================================
N = 4
print(f"✅ Запуск программы с параметром N = {N}")

n_vec = list(range(1, 100_000 * N + 1, 100 * N))
n_mat = list(range(20, 301, 20))

# =============================================================================
# 4. Замеры
# =============================================================================
print("🚀 Замеры векторных операций...")
t2, t4, t5, t8 = [], [], [], []
for n in n_vec:
    v = [random.uniform(1.0, 100.0) for _ in range(n)]
    t2.append(m_f2(v))
    t4.append(m_f4(v))
    t5.append(m_f5(v))
    t8.append(m_f8(v))
    if n % 40_000 == 0:
        print(f"   [Векторы] n = {n}")

print(" Замеры матричного умножения...")
t_mat = []
for n in n_mat:
    A = [[random.uniform(0.1, 10.0) for _ in range(n)] for _ in range(n)]
    B = [[random.uniform(0.1, 10.0) for _ in range(n)] for _ in range(n)]
    t_mat.append(m_mat(A, B, n))
    print(f"   [Матрицы] n = {n}")

# =============================================================================
# 5. Экспорт в Excel (.xlsx)
# =============================================================================
# --- Файл 1: vector_results.xlsx ---
wb_vec = openpyxl.Workbook()
ws_vec = wb_vec.active
ws_vec.title = "Vector Results"
ws_vec.append(['n', 'f2_sum_sec', 'f4_horner_sec', 'f5_max_sec', 'f8_harmonic_sec'])
for i in range(len(n_vec)):
    ws_vec.append([n_vec[i], t2[i], t4[i], t5[i], t8[i]])
wb_vec.save('vector_results.xlsx')
print("✅ Сохранено: vector_results.xlsx")

# --- Файл 2: matrix_results.xlsx ---
wb_mat = openpyxl.Workbook()
ws_mat = wb_mat.active
ws_mat.title = "Matrix Results"
ws_mat.append(['n', 'mat_mult_sec'])
for i in range(len(n_mat)):
    ws_mat.append([n_mat[i], t_mat[i]])
wb_mat.save('matrix_results.xlsx')
print("✅ Сохранено: matrix_results.xlsx")

# =============================================================================
# 6. Построение и сохранение графиков
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

ax1.plot(n_vec, t2, 'o-', label='f2: Сумма')
ax1.plot(n_vec, t4, 's-', label='f4: Горнер')
ax1.plot(n_vec, t5, '^-', label='f5: Максимум')
ax1.plot(n_vec, t8, 'd-', label='f8: Гарм. среднее')
ax1.set_title('Задание 1: Векторные операции (O(n))')
ax1.set_xlabel('n (размер вектора)')
ax1.set_ylabel('Время, сек')
ax1.grid(True)
ax1.legend()

ax2.plot(n_mat, t_mat, 'r^-', label='Умножение матриц')
ax2.set_title('Задание 2: Матричное умножение (O(n^3))')
ax2.set_xlabel('n (размер матрицы)')
ax2.set_ylabel('Время, сек')
ax2.grid(True)
ax2.legend()

plt.tight_layout()

# ВАЖНО: сохраняем ДО plt.show(), иначе файл будет пустым
fig.savefig('lab01_results_var24.png', dpi=150, bbox_inches='tight')
print("✅ Графики сохранены в lab01_results_var24.png")

plt.show()