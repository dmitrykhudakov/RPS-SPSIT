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
            
            numbers = []
            parts = input_str.split()
            
            for part in parts:
                num = int(part)
                if num < -1000000 or num > 1000000:
                    print(f"Ошибка: число {num} выходит за допустимые пределы!")
                    print("Допустимый диапазон: от -1,000,000 до 1,000,000")
                    raise ValueError
                numbers.append(num)
            
            print(f"\n✓ Массив успешно введен!")
            print(f"Количество элементов: {len(numbers)}")
            print(f"Введенный массив: {' '.join(map(str, numbers))}")
            
            return numbers
        except ValueError as e:
            if "выходит за допустимые пределы" in str(e):
                continue
            print("Ошибка: вводите только целые числа!")
        except KeyboardInterrupt:
            print("\n\nВвод прерван.")
            return []


def generate_random_array():
    print("\nГЕНЕРАЦИЯ СЛУЧАЙНОГО МАССИВА")
    print("-" * 40)
    print("Ограничения:")
    print("• Размер массива: 1-1000")
    print("• Допустимый диапазон: от -1,000,000 до 1,000,000")
    print("-" * 40)
    
    while True:
        try:
            size = int(input("Введите размер массива (1-1000): "))
            if size < 1 or size > 1000:
                print("Размер должен быть от 1 до 1000!")
                continue
            
            while True:
                try:
                    min_val = int(input("Введите минимальное значение: "))
                    if min_val < -1000000:
                        print(f"Ошибка: минимальное значение не может быть меньше -1,000,000")
                        continue
                    break
                except ValueError:
                    print("Ошибка: вводите только целые числа!")
            
            while True:
                try:
                    max_val = int(input("Введите максимальное значение: "))
                    if max_val > 1000000:
                        print(f"Ошибка: максимальное значение не может быть больше 1,000,000")
                        continue
                    break
                except ValueError:
                    print("Ошибка: вводите только целые числа!")
            
            if min_val > max_val:
                print("Минимальное значение должно быть меньше максимального!")
                continue
            
            arr = [random.randint(min_val, max_val) for _ in range(size)]
            
            print(f"\n✓ Массив успешно сгенерирован!")
            print(f"Количество элементов: {size}")
            
            print(f"\nСгенерированный массив (все {size} элементов):")
            print_full_array(arr)
            
            return arr
        except ValueError:
            print("Ошибка: вводите только целые числа!")
        except KeyboardInterrupt:
            print("\n\nГенерация прервана.")
            return []


def load_array_from_file():
    print("\nЗАГРУЗКА МАССИВА ИЗ ФАЙЛА")
    print("-" * 40)
    print("Ограничение: каждое число должно быть в пределах")
    print("от -1,000,000 до 1,000,000")
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
                            num = int(part)
                            if num < -1000000 or num > 1000000:
                                print(f"Ошибка: число {num} в файле выходит за допустимые пределы!")
                                print("Допустимый диапазон: от -1,000,000 до 1,000,000")
                                return []
                            numbers.append(num)
            
            if not numbers:
                print("Файл не содержит допустимых чисел!")
                return []
            
            print(f"\n✓ Массив успешно загружен из файла '{filename}'")
            print(f"Количество элементов: {len(numbers)}")
            
            print(f"\nЗагруженный массив (все {len(numbers)} элементов):")
            print_full_array(numbers)
            
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


def save_arrays_to_file(original_arr, sorted_arr, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("ИСХОДНЫЙ МАССИВ:\n")
            file.write('[' + ', '.join(map(str, original_arr)) + ']\n\n')
            
            if sorted_arr:
                file.write("ОТСОРТИРОВАННЫЙ МАССИВ:\n")
                file.write('[' + ', '.join(map(str, sorted_arr)) + ']\n')
        
        print(f"✓ Оба массива сохранены в файл: {filename}")
        print(f"  Размер файла: {os.path.getsize(filename)} байт")
        
    except Exception as e:
        print(f"✗ Ошибка при сохранении файла: {e}")


def print_full_array(arr):
    if not arr:
        print("(пустой массив)")
        return
    
    if len(arr) <= 50:
        print(' '.join(map(str, arr)))
    else:
        elements_per_line = 10
        for i in range(0, len(arr), elements_per_line):
            chunk = arr[i:i+elements_per_line]
            print(' '.join(f"{num:8}" for num in chunk))


def display_array(arr, name="Массив"):
    print(f"\n{name} ({len(arr)} элементов):")
    print("-" * 40)
    
    if not arr:
        print("(пустой)")
        return
    
    print_full_array(arr)
    
    print(f"\nВсего элементов: {len(arr)}")


def print_current_array_info(arr):
    if not arr:
        print("\nТекущий массив: не задан")
        return
    
    print(f"\nТЕКУЩИЙ МАССИВ ({len(arr)} элементов):")
    
    if len(arr) <= 30:
        print(f"Элементы: {' '.join(map(str, arr))}")
    else:
        print("Все элементы:")
        elements_per_line = 10
        for i in range(0, len(arr), elements_per_line):
            chunk = arr[i:i+elements_per_line]
            print(' '.join(f"{num:8}" for num in chunk))


def main():
    clear_screen()
    print_header()
    
    original_array = []
    sorted_array = []
    
    while True:
        clear_screen()
        print_header()
        
        print_current_array_info(original_array)
        
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 60)
        print("1. Ввод массива с клавиатуры")
        print("2. Генерация случайного массива")
        print("3. Загрузка массива из файла")
        print("4. Выполнить сортировку")
        print("5. Сохранить массивы в файл")
        print("6. Очистить текущий массив")
        print("7. Выход")
        print("=" * 60)
        
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
                    input("\nНажмите Enter для продолжения...")
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
                
                input("\nНажмите Enter для возврата в меню...")
                    
            elif choice == '5':
                if not original_array:
                    print("\nНет данных для сохранения!")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                print("\nСОХРАНЕНИЕ МАССИВОВ В ФАЙЛ")
                print("-" * 40)
                
                default_name = "sorted_array_result.txt"
                filename = input(f"Введите имя файла (по умолчанию '{default_name}'): ")
                
                if not filename.strip():
                    filename = default_name
                
                save_arrays_to_file(original_array, sorted_array, filename)
                
                print(f"\nСодержимое файла '{filename}':")
                print("=" * 40)
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        print(file.read())
                except Exception as e:
                    print(f"Не удалось прочитать файл: {e}")
                
                input("\nНажмите Enter для возврата в меню...")
                    
            elif choice == '6':
                original_array = []
                sorted_array = []
                print("\nТекущий массив очищен.")
                input("\nНажмите Enter для продолжения...")
                
            elif choice == '7':
                print("\nВыход из программы...")
                print("Спасибо за использование!")
                break
                
            else:
                print("Неверный выбор! Введите число от 1 до 7.")
                input("\nНажмите Enter для продолжения...")
                
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена.")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        input("Нажмите Enter для выхода...")