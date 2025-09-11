"""
Python має дві вбудовані функції сортування: sorted і sort. Функції сортування Python використовують Timsort — 
гібридний алгоритм сортування, що поєднує в собі сортування злиттям і сортування вставками.

Порівняйте три алгоритми сортування: злиттям, вставками та Timsort за часом виконання. 
Аналіз повинен бути підтверджений емпіричними даними, отриманими шляхом тестування алгоритмів на різних наборах даних. 
Емпірично перевірте теоретичні оцінки складності алгоритмів, наприклад, сортуванням на великих масивах. 
Для заміру часу виконання алгоритмів використовуйте модуль timeit.

Покажіть, що поєднання сортування злиттям і сортування вставками робить алгоритм Timsort набагато ефективнішим, 
і саме з цієї причини програмісти, в більшості випадків, використовують вбудовані в Python алгоритми, 
а не кодують самі. Зробіть висновки.
"""

import random, timeit
from typing import List, Callable, Dict, Tuple

# Алгоритми 

def insertion_sort(a):
    arr = a[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(a):
    n = len(a)
    if n <= 1: return a[:]
    mid = n // 2
    L = merge_sort(a[:mid])
    R = merge_sort(a[mid:])
    i = j = 0
    out = []
    append = out.append
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: append(L[i]); i += 1
        else:            append(R[j]); j += 1
    if i < len(L): out.extend(L[i:])
    if j < len(R): out.extend(R[j:])
    return out

def timsort_builtin(a: List[int]) -> List[int]:
    return sorted(a)

ALGOS = {
    "Insertion": insertion_sort,
    "Merge": merge_sort,
    "Timsort": timsort_builtin,
}

# Генерація даних 
def gen_random(n, seed = 42):
    rng = random.Random(seed)
    return [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]

def gen_sorted(n):
    return list(range(n))

def gen_reversed(n):
    return list(range(n, 0, -1))

def gen_nearly_sorted(n, swaps = None, seed = 123):
    if swaps is None: swaps = max(1, n // 100)  # 1% свапів
    a = list(range(n))
    rng = random.Random(seed)
    for _ in range(swaps):
        i, j = rng.randrange(n), rng.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a

DATASETS = [
    ("Random", gen_random),
    ("Sorted", gen_sorted),
    ("Reversed", gen_reversed),
    ("Nearly-sorted (1%)", gen_nearly_sorted),
]

# Порівняльне тестування
def time_median(fn, data, repeats):
    t = timeit.repeat(lambda: fn(data), number=1, repeat=repeats)
    t.sort()
    return t[len(t)//2]

def main():
    # self-test
    _test = [5, 1, 4, -3, 2, 0]
    for f in (insertion_sort, merge_sort, timsort_builtin):
        assert f(_test) == sorted(_test)

    # налаштування
    SIZES = [500, 2000, 5000]
    REPEATS = 5
    INSERTION_MAX = 5000

    rows = []
    for ds_name, gen in DATASETS:
        base = gen(max(SIZES))
        for n in SIZES:
            arr = base[:n]
            for name, fn in ALGOS.items():
                if name == "Insertion" and n > INSERTION_MAX:
                    continue
                t = time_median(fn, arr, REPEATS)
                rows.append({"dataset": ds_name, "n": n, "algo": name, "time_s": t})

    # відносно Timsort
    timsort_time = {}
    for r in rows:
        if r["algo"] == "Timsort":
            timsort_time[(r["dataset"], r["n"])] = r["time_s"]
    for r in rows:
        base = timsort_time.get((r["dataset"], r["n"]))
        r["x_slower_vs_timsort"] = (r["time_s"]/base) if base and base > 0 else None

    # Початкові вимірювання
    print("=== Початкові вимірювання (медіанний час, с) ===")
    header = f"{'dataset':22} {'n':>7} {'algo':10} {'time_s':>10} {'x_slower_vs_timsort':>22}"
    print(header)
    print("-" * len(header))
    for r in rows:
        xs = f"{r['x_slower_vs_timsort']:.2f}x" if r['x_slower_vs_timsort'] is not None else "-"
        print(f"{r['dataset']:22} {r['n']:7d} {r['algo']:10} {r['time_s']:10.6f} {xs:>22}")

    # Зведена таблиця
    print("\n=== Зведена таблиця (dataset × n): час і «x повільніше за Timsort» ===")
    keys = sorted({(r["dataset"], r["n"]) for r in rows}, key=lambda x:(x[0], x[1]))
    for ds, n in keys:
        subset = {r["algo"]: r for r in rows if r["dataset"]==ds and r["n"]==n}
        def fmt(name):
            r = subset.get(name)
            if not r: return "—"
            xs = r['x_slower_vs_timsort']
            return f"{r['time_s']:.6f}s" if xs is None else f"{r['time_s']:.6f}s ({xs:.2f}x)"
        print(
    f"{ds:22} n={n:5d} | "
    f"Insertion: {fmt('Insertion'):<26} | "
    f"Merge: {fmt('Merge'):<26} | "
    f"Timsort: {fmt('Timsort'):<26}"
)

    # Висновки
    avg_slowdown: Dict[str,float] = {}
    cnt: Dict[str,int] = {}
    for r in rows:
        x = r["x_slower_vs_timsort"]
        if x is None: continue
        name = r["algo"]
        avg_slowdown[name] = avg_slowdown.get(name,0.0) + x
        cnt[name] = cnt.get(name,0) + 1

    print("\n=== Висновки ===")
    for name in sorted(avg_slowdown, key=lambda k: avg_slowdown[k]/cnt[k]):
        if name == "Timsort":
            print("- Timsort — база для порівняння (найшвидший у більшості випадків).")
        else:
            print(f"- {name}: у середньому повільніший за Timsort у {(avg_slowdown[name]/cnt[name]):.1f}×")

if __name__ == "__main__":
    main()
