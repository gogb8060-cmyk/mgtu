"""
Лабораторная работа №2. Алгоритмы сортировки.
Вариант: 4 | Алгоритмы: Быстрая (Хоара), Сортировка перемешиванием (шейкерная)

Замеры времени для трёх типов массивов: случайный, упорядоченный, обратный.
Для шейкерной сортировки на n=100000 (кроме упорядоченного) замер пропускается,
так как квадратичный алгоритм O(n²) в Python займёт 15-30 минут.
"""

import random
import timeit
import matplotlib.pyplot as plt

# Попытка импорта get_usage_time из первой лабы
try:
    from usage_time import get_usage_time
    HAS_USAGE_TIME = True
except ImportError:
    HAS_USAGE_TIME = False
    print("⚠️  usage_time не найден — используется timeit")


# 1. Алгоритмы сортировки (Вариант 4)

def quick_sort_hoare(arr):
    """Быстрая сортировка (схема Хоара). O(n log n) в среднем."""
    a = list(arr)  # Копия, чтобы не мутировать исходный массив
    _quick_sort_hoare(a, 0, len(a) - 1)
    return a

def _quick_sort_hoare(a, low, high):
    if low < high:
        p = _partition_hoare(a, low, high)
        _quick_sort_hoare(a, low, p)
        _quick_sort_hoare(a, p + 1, high)

def _partition_hoare(a, low, high):
    pivot = a[low + (high - low) // 2]  # Средний элемент как опорный
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def cocktail_shaker_sort(arr):
    """Сортировка перемешиванием (шейкерная). O(n²)."""
    a = list(arr)
    n = len(a)
    swapped = True
    begin = 0
    end = n - 1
    while swapped:
        swapped = False
        # Проход слева направо (всплывает максимум)
        for i in range(begin, end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        # Проход справа налево (всплывает минимум)
        for i in range(end - 1, begin - 1, -1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        begin += 1
    return a


# 2. Настройка замеров

if HAS_USAGE_TIME:
    measure_small = get_usage_time(number=3, ndigits=6)
    measure_large = get_usage_time(number=1, ndigits=6)
    
    m_quick_small   = measure_small(quick_sort_hoare)
    m_cocktail_small = measure_small(cocktail_shaker_sort)
    m_quick_large   = measure_large(quick_sort_hoare)
    m_cocktail_large = measure_large(cocktail_shaker_sort)
else:
    def make_timer(func, number=1):
        def timer(arr):
            return timeit.timeit(lambda: func(arr), number=number) / number
        return timer
    
    m_quick_small    = make_timer(quick_sort_hoare, number=3)
    m_cocktail_small = make_timer(cocktail_shaker_sort, number=3)
    m_quick_large    = make_timer(quick_sort_hoare, number=1)
    m_cocktail_large = make_timer(cocktail_shaker_sort, number=1)


# 3. Параметры эксперимента
sizes = [1000, 5000, 10000, 100000]
array_types = ['random', 'sorted', 'reverse']
type_names = {
    'random':  'Случайный',
    'sorted':  'Упорядоченный',
    'reverse': 'Обратный'
}

SEED = 42
random.seed(SEED)

results = []  # Список словарей для построения графиков


# 4. Генерация массивов
def generate_array(n, arr_type):
    """Генерирует массив заданного размера и типа."""
    arr = [random.randint(1, 1_000_000) for _ in range(n)]
    if arr_type == 'sorted':
        arr.sort()
    elif arr_type == 'reverse':
        arr.sort(reverse=True)
    return arr


# 5. Замеры
print("=" * 78)
print(" Лабораторная работа №2. Алгоритмы сортировки. Вариант 4")
print(" Алгоритмы: Быстрая (Хоара)  vs  Сортировка перемешиванием")
print("=" * 78)

for n in sizes:
    print(f"\n--- Размер массива: n = {n:,} ---")
    
    # Адаптивный выбор измерителя
    m_quick    = m_quick_small    if n <= 10000 else m_quick_large
    m_cocktail = m_cocktail_small if n <= 10000 else m_cocktail_large
    
    for arr_type in array_types:
        original = generate_array(n, arr_type)
        
        # --- Быстрая сортировка (замеряем всегда) ---
        t_quick = m_quick(original)
        
        # --- Шейкерная сортировка ---
        # Пропускаем для n=100000 на случайном и обратном массивах (O(n²) ≈ 15-30 мин)
        skip_cocktail = (n == 100000 and arr_type != 'sorted')
        
        if skip_cocktail:
            t_cocktail = None
            print(f"  {type_names[arr_type]:<15} | Quick: {t_quick:<10.6f} с | Cocktail: пропущен (O(n²) в Python ≈ 15+ мин)")
        else:
            if n == 100000:
                print(f"  {type_names[arr_type]:<15} | замер Cocktail...", end=' ', flush=True)
            t_cocktail = m_cocktail(original)
            print(f"  {type_names[arr_type]:<15} | Quick: {t_quick:<10.6f} с | Cocktail: {t_cocktail:<10.6f} с")
        
        results.append({
            'n': n,
            'type': type_names[arr_type],
            'quick_sec': t_quick,
            'cocktail_sec': t_cocktail,
        })


# 6. Построение и сохранение графиков
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Сравнение алгоритмов сортировки (Вариант 4)\n'
             'Быстрая (Хоара)  vs  Сортировка перемешиванием',
             fontsize=13, fontweight='bold', y=1.02)

colors = {'quick': '#2196F3', 'cocktail': '#F44336'}

for idx, arr_type in enumerate(array_types):
    ax = axes[idx]
    
    # Фильтруем результаты по типу массива
    subset = [r for r in results if r['type'] == type_names[arr_type]]
    
    ns_all       = [r['n'] for r in subset]
    t_quick      = [r['quick_sec'] for r in subset]
    t_cocktail   = [r['cocktail_sec'] for r in subset]
    
    # Для шейкерной убираем None (пропущенные замеры)
    ns_cocktail  = [r['n'] for r in subset if r['cocktail_sec'] is not None]
    t_cocktail_f = [r['cocktail_sec'] for r in subset if r['cocktail_sec'] is not None]
    
    # Быстрая сортировка — всегда 4 точки
    ax.plot(ns_all, t_quick, 'o-', label='Быстрая (Хоара)', color=colors['quick'],
            markersize=8, linewidth=2, zorder=5)
    
    # Шейкерная — 3 или 4 точки (зависит от пропуска)
    if t_cocktail_f:
        ax.plot(ns_cocktail, t_cocktail_f, 's-', label='Перемешиванием',
                color=colors['cocktail'], markersize=8, linewidth=2, zorder=5)
    
    # Подписи значений на точках
    for x, y in zip(ns_all, t_quick):
        ax.annotate(f'{y:.4f}', (x, y), textcoords="offset points",
                    xytext=(0, 12), ha='center', fontsize=7, color=colors['quick'])
    for x, y in zip(ns_cocktail, t_cocktail_f):
        ax.annotate(f'{y:.3f}', (x, y), textcoords="offset points",
                    xytext=(0, -14), ha='center', fontsize=7, color=colors['cocktail'])
    
    # Аннотация о пропуске
    if arr_type != 'sorted':
        ax.text(0.98, 0.02, 'O(n²) на n=100000\nпропущен',
                transform=ax.transAxes, fontsize=8, verticalalignment='bottom',
                horizontalalignment='right', color='gray',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_title(f'Тип массива: {type_names[arr_type]}', fontsize=12, fontweight='bold')
    ax.set_xlabel('n (размер массива)', fontsize=10)
    ax.set_ylabel('Время, сек', fontsize=10)
    ax.set_xscale('linear')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10, loc='upper left')

plt.tight_layout()

filename = 'lab02_sorting_results_var4.png'
fig.savefig(filename, dpi=150, bbox_inches='tight')
print(f"\n✅ Графики сохранены: {filename}")
print("   (Вставь этот файл в раздел «Результаты выполнения» отчёта)")

plt.show()