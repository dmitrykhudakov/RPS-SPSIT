import random
import os
import sys
from bucket_sort import bucket_sort


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 60)
    print("       ПРИЛОЖЕНИЕ ДЛЯ БЛОЧНОЙ СОРТИРОВКИ (BUCKET SORT)")
    print("=" * 60)
    print("Вариант 21 | Худяков Дмитрий")
    print()


def input_array_from_keyboard():
    print("\nВВОД МАССИВА С КЛАВИАТУРЫ")
    print("-" * 40)
    
    while True:
        try:
            input_str = input("Введите числа через пробел: ")
            if not input_str.strip():
                print("Ошибка: введите хотя бы одно число!")
                continue
            
            numbers = list(map(int, input_str.split()))
            return numbers
        except ValueError:
            print("Ошибка: вводите только целые числа!")
        except KeyboardInterrupt:
            print("\n\nВвод прерван.")
            return []


def generate_random_array():
    print("\nГЕНЕРАЦИЯ СЛУЧАЙНОГО МАССИВА")
    print("-" * 40)
    
    while True:
        try:
            size = int(input("Введите размер массива (1-1000): "))
            if size < 1 or size > 1000:
                print("Размер должен быть от 1 до 1000!")
                continue
            
            min_val = int(input("Введите минимальное значение: "))
            max_val = int(input("Введите максимальное значение: "))
            
            if min_val > max_val:
                print("Минимальное значение должно быть меньше максимального!")
                continue
            
            arr = [random.randint(min_val, max_val) for _ in range(size)]
            return arr
        except ValueError:
            print("Ошибка: вводите только целые числа!")
        except KeyboardInterrupt:
            print("\n\nГенерация прервана.")
            return []


def load_array_from_file():
    print("\nЗАГРУЗКА МАССИВА ИЗ ФАЙЛА")
    print("-" * 40)
    
    filename = input("Введите имя файла (например, 'array.txt'): ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print("Файл пуст!")
                return []
            
            lines = content.split('\n')
            numbers = []
            
            for line in lines:
                line = line.strip('[]()')
                if line:
                    parts = line.replace(',', ' ').split()
                    for part in parts:
                        if part:
                            numbers.append(int(part))
            
            print(f"Загружено {len(numbers)} чисел из файла '{filename}'")
            return numbers
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return []
    except ValueError:
        print("Ошибка: файл должен содержать только целые числа!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def save_array_to_file(arr, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('[' + ', '.join(map(str, arr)) + ']')
        print(f"Массив сохранен в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


def display_array(arr, name="Массив"):
    print(f"\n{name} ({len(arr)} элементов):")
    print("-" * 40)
    
    if not arr:
        print("(пустой)")
        return
    
    if len(arr) <= 20:
        print(' '.join(map(str, arr)))
    else:
        for i in range(0, len(arr), 10):
            chunk = arr[i:i+10]
            print(' '.join(f"{num:6}" for num in chunk))
    
    print(f"\nВсего элементов: {len(arr)}")


def main():
    clear_screen()
    print_header()
    
    original_array = []
    sorted_array = []
    
    while True:
        print("\nГЛАВНОЕ МЕНЮ")
        print("-" * 40)
        print("1. Ввод массива с клавиатуры")
        print("2. Генерация случайного массива")
        print("3. Загрузка массива из файла")
        print("4. Выполнить сортировку")
        print("5. Сохранить массивы в файлы")
        print("6. Очистить экран")
        print("7. Выход")
        print("-" * 40)
        
        if original_array:
            print(f"Текущий массив: {len(original_array)} элементов")
        
        try:
            choice = input("\nВыберите действие (1-7): ")
            
            if choice == '1':
                original_array = input_array_from_keyboard()
                sorted_array = []
                
            elif choice == '2':
                original_array = generate_random_array()
                sorted_array = []
                
            elif choice == '3':
                original_array = load_array_from_file()
                sorted_array = []
                
            elif choice == '4':
                if not original_array:
                    print("\nСначала введите или загрузите массив!")
                    continue
                
                print("\nВЫПОЛНЕНИЕ СОРТИРОВКИ")
                print("-" * 40)
                
                display_array(original_array, "Исходный массив")
                
                print("\nСортировка...")
                try:
                    sorted_array = bucket_sort(original_array)
                    
                    display_array(sorted_array, "Отсортированный массив")
                    
                    if sorted_array == sorted(original_array):
                        print("\n✓ Сортировка выполнена корректно!")
                    else:
                        print("\n⚠ Внимание: результат сортировки может содержать ошибки!")
                        
                except Exception as e:
                    print(f"\n✗ Ошибка при сортировке: {e}")
                    sorted_array = []
                    
            elif choice == '5':
                if not original_array:
                    print("\nНет данных для сохранения!")
                    continue
                
                print("\nСОХРАНЕНИЕ В ФАЙЛЫ")
                print("-" * 40)
                
                base_name = input("Введите базовое имя для файлов (без расширения): ")
                if not base_name:
                    base_name = "array"
                
                if original_array:
                    save_array_to_file(original_array, f"{base_name}_original.txt")
                
                if sorted_array:
                    save_array_to_file(sorted_array, f"{base_name}_sorted.txt")
                else:
                    print("Отсортированный массив не найден. Сначала выполните сортировку.")
                    
            elif choice == '6':
                clear_screen()
                print_header()
                
            elif choice == '7':
                print("\nВыход из программы...")
                print("Спасибо за использование!")
                break
                
            else:
                print("Неверный выбор! Введите число от 1 до 7.")
                
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            
        if choice not in ['6', '7']:
            input("\nНажмите Enter для продолжения...")
            clear_screen()
            print_header()
            if original_array:
                print(f"Текущий массив: {len(original_array)} элементов")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена.")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        input("Нажмите Enter для выхода...")