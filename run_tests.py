import time
import random
import sys
import os
from bucket_sort import bucket_sort


def print_header(title):
    """Печать заголовка теста"""
    print(f"\n{title}")
    print("=" * 60)


def test_all_same_elements():
    """Тест: все элементы одинаковые (оптимизированный случай)"""
    print_header("ТЕСТИРОВАНИЕ ВРЕМЕННОЙ СЛОЖНОСТИ BUCKET SORT")
    print_header("Тест: все элементы одинаковые (оптимизированный случай)")
    print("Ожидаемая сложность: O(n) благодаря оптимизации")
    print("=" * 60)
    
    sizes = [1000, 5000, 10000, 50000, 100000]
    times = []
    
    for size in sizes:
        # Создаем массив с одинаковыми элементами
        arr = [42] * size
        
        # Замеряем время сортировки
        start_time = time.perf_counter()
        bucket_sort(arr)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"| Размер:    | {size:<6} | Время: {elapsed_time:.6f} сек |")
    
    print()
    print("Анализ роста времени:")
    
    # Анализ роста времени
    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[0]
        time_ratio = times[i] / times[0]
        print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз")


def test_random_uniform():
    """Тест: случайные числа с равномерным распределением"""
    print_header("\nТест: случайные числа (равномерное распределение)")
    print("Ожидаемая сложность: O(n + k) ≈ O(n)")
    print("=" * 60)
    
    sizes = [500, 1000, 2500, 5000, 10000]
    times = []
    
    for size in sizes:
        # Создаем массив со случайными числами от 0 до 1000
        arr = [random.randint(0, 1000) for _ in range(size)]
        
        # Замеряем время сортировки
        start_time = time.perf_counter()
        bucket_sort(arr)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"| Размер:    | {size:<6} | Время: {elapsed_time:.6f} сек |")
    
    print()
    print("Анализ роста времени:")
    
    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[0]
        time_ratio = times[i] / times[0]
        if i < len(sizes) - 1:
            print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз")
        else:
            print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз")


def test_worst_case_small_range():
    """Тест: худший случай - маленький диапазон значений"""
    print_header("\nТест: маленький диапазон значений (почти худший случай)")
    print("Ожидаемая сложность: O(n²) в теории, но на практике лучше")
    print("=" * 60)
    
    sizes = [100, 500, 1000, 2000, 4000]
    times = []
    
    for size in sizes:
        # Создаем массив со значениями только 0, 1, 2
        arr = [random.randint(0, 2) for _ in range(size)]
        
        # Замеряем время сортировки
        start_time = time.perf_counter()
        bucket_sort(arr)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"| Размер:    | {size:<6} | Время: {elapsed_time:.6f} сек |")
    
    print()
    print("Анализ роста времени:")
    
    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[0]
        time_ratio = times[i] / times[0]
        quadratic_ratio = size_ratio ** 2
        print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз (квадратичный рост: {quadratic_ratio:.1f})")


def test_sorted_array():
    """Тест: уже отсортированный массив"""
    print_header("\nТест: уже отсортированный массив")
    print("Ожидаемая сложность: O(n) - хороший случай")
    print("=" * 60)
    
    sizes = [1000, 5000, 10000, 25000, 50000]
    times = []
    
    for size in sizes:
        # Создаем уже отсортированный массив
        arr = list(range(size))
        
        # Замеряем время сортировки
        start_time = time.perf_counter()
        bucket_sort(arr)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"| Размер:    | {size:<6} | Время: {elapsed_time:.6f} сек |")
    
    print()
    print("Анализ роста времени:")
    
    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[0]
        time_ratio = times[i] / times[0]
        print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз")


def test_reverse_sorted():
    """Тест: массив в обратном порядке"""
    print_header("\nТест: массив в обратном порядке")
    print("Ожидаемая сложность: O(n²) в теории")
    print("=" * 60)
    
    sizes = [500, 1000, 2000, 4000, 8000]
    times = []
    
    for size in sizes:
        # Создаем массив в обратном порядке
        arr = list(range(size, 0, -1))
        
        # Замеряем время сортировки
        start_time = time.perf_counter()
        bucket_sort(arr)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"| Размер:    | {size:<6} | Время: {elapsed_time:.6f} сек |")
    
    print()
    print("Анализ роста времени:")
    
    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[0]
        time_ratio = times[i] / times[0]
        quadratic_ratio = size_ratio ** 2
        print(f"Увеличение размера в {size_ratio:.1f} раз -> время увеличилось в {time_ratio:.1f} раз (квадратичный: {quadratic_ratio:.1f})")


def compare_with_builtin():
    """Сравнение с встроенной сортировкой Python"""
    print_header("\nСРАВНЕНИЕ С ВСТРОЕННОЙ СОРТИРОВКОЙ PYTHON")
    print("=" * 60)
    
    sizes = [1000, 5000, 10000, 50000, 100000]
    
    print(f"{'Размер':<10} | {'Bucket Sort':<12} | {'sorted()':<12} | {'Отношение':<10}")
    print("-" * 50)
    
    for size in sizes:
        # Создаем случайный массив
        arr = [random.randint(-10000, 10000) for _ in range(size)]
        arr_copy = arr.copy()
        
        # Замер Bucket Sort
        start_time1 = time.perf_counter()
        bucket_sort(arr)
        end_time1 = time.perf_counter()
        time1 = end_time1 - start_time1
        
        # Замер встроенной сортировки
        start_time2 = time.perf_counter()
        sorted(arr_copy)
        end_time2 = time.perf_counter()
        time2 = end_time2 - start_time2
        
        ratio = time1 / time2 if time2 > 0 else 0
        
        print(f"{size:<10} | {time1:.6f} сек  | {time2:.6f} сек  | {ratio:.2f}x")


def summary():
    """Итоговый анализ сложности"""
    print_header("\nИТОГОВЫЙ АНАЛИЗ СЛОЖНОСТИ BUCKET SORT")
    print("=" * 60)
    
    print("\nЛУЧШИЕ СЛУЧАИ (O(n) или O(n + k)):")
    print("✓ Все элементы одинаковые")
    print("✓ Уже отсортированный массив")
    print("✓ Равномерное распределение значений")
    
    print("\nХУДШИЕ СЛУЧАИ (O(n²)):")
    print("✗ Все элементы в одном блоке (малый диапазон)")
    print("✗ Обратно отсортированный массив")
    print("✗ Неравномерное распределение")
    
    print("\nПРОСТРАНСТВЕННАЯ СЛОЖНОСТЬ:")
    print("• O(n + k) - требуется дополнительная память для блоков")
    print("• k = n в нашей реализации")
    
    print("\nПРАКТИЧЕСКИЕ ВЫВОДЫ:")
    print("1. Bucket Sort эффективен при равномерном распределении данных")
    print("2. В худшем случае может быть медленнее квадратичных алгоритмов")
    print("3. Хорошо подходит для сортировки чисел с известным диапазоном")
    print("4. В среднем быстрее квадратичных сортировок, но медленнее быстрой сортировки")


def main():
    """Основная функция программы тестирования сложности"""
    print("=" * 60)
    print("   ТЕСТИРОВАНИЕ ВРЕМЕННОЙ СЛОЖНОСТИ BUCKET SORT")
    print("=" * 60)
    print("Вариант 21 | Худяков Дмитрий")
    print()
    
    try:
        # Запуск всех тестов
        test_all_same_elements()
        test_random_uniform()
        test_worst_case_small_range()
        test_sorted_array()
        test_reverse_sorted()
        compare_with_builtin()
        summary()
        
        print("\n" + "=" * 60)
        print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ Ошибка: не удалось импортировать bucket_sort: {e}")
        print("Убедитесь, что файл bucket_sort.py находится в той же директории")
        return 1
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    input("\nНажмите Enter для выхода...")
    sys.exit(exit_code)