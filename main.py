"""
GUI приложение для сортировки массивов алгоритмом Bucket Sort.

Использует Tkinter для создания графического интерфейса.
Включает систему авторизации и сохранение истории сортировок в базе данных.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import random
from bucket_sort import bucket_sort
from auth import AuthManager


class BucketSortApp:
    """Класс для работы с алгоритмом Bucket Sort."""
    
    MAX_ARRAY_SIZE = 1000  # Максимальный размер массива
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bucket Sort - Сортировка массивов")
        self.root.geometry("900x700")
        self.root.configure(bg='#ffffff')
        
        # Менеджер аутентификации
        self.auth_manager = AuthManager()
        
        # Данные
        self.original_array = []
        self.sorted_array = None
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Обновляем статус авторизации
        self.update_auth_status()
    
    def show_login_dialog(self):
        """Показывает диалог авторизации."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Авторизация")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        
        # Центрируем окно
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"450x350+{x}+{y}")
        
        # Заголовок
        title_frame = tk.Frame(dialog, bg='#2c3e50')
        title_frame.pack(fill='x')
        title_label = tk.Label(
            title_frame,
            text="Вход в систему",
            font=('Segoe UI', 18, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # Поля ввода
        content_frame = tk.Frame(dialog, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        tk.Label(
            content_frame,
            text="Имя пользователя:",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(10, 5))
        
        username_entry = tk.Entry(
            content_frame,
            font=('Segoe UI', 12),
            width=30,
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        username_entry.pack(fill='x', pady=5)
        username_entry.focus()
        
        tk.Label(
            content_frame,
            text="Пароль:",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(15, 5))
        
        password_entry = tk.Entry(
            content_frame,
            font=('Segoe UI', 12),
            width=30,
            show='*',
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        password_entry.pack(fill='x', pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.login(username, password)
            if success:
                dialog.destroy()
                self.update_auth_status()
                messagebox.showinfo("Успех", msg)
            else:
                messagebox.showerror("Ошибка", msg)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.register(username, password)
            if success:
                messagebox.showinfo("Успех", msg)
                # Автоматически входим после регистрации
                success, msg = self.auth_manager.login(username, password)
                if success:
                    dialog.destroy()
                    self.update_auth_status()
                    messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            else:
                messagebox.showerror("Ошибка", msg)
        
        # Кнопки
        button_frame = tk.Frame(content_frame, bg='#ecf0f1')
        button_frame.pack(pady=10)
        
        # Создаем невидимое изображение для задания размеров в пикселях
        pixel = tk.PhotoImage(width=1, height=1)
        
        # Кнопка "Войти"
        login_container = tk.Frame(button_frame, bg='#27ae60', width=130, height=50)
        login_container.pack_propagate(False)  # Запрещаем изменение размера
        login_container.pack(side='left', padx=15)
        
        btn_login = tk.Button(
            login_container,
            text="Войти",
            command=login,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        )
        btn_login.pack(fill='both', expand=True)
        
        # Кнопка "Регистрация"
        register_container = tk.Frame(button_frame, bg='#3498db', width=160, height=50)
        register_container.pack_propagate(False)  # Запрещаем изменение размера
        register_container.pack(side='left', padx=15)
        
        btn_register = tk.Button(
            register_container,
            text="Регистрация",
            command=register,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 12),
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white'
        )
        btn_register.pack(fill='both', expand=True)
        
        password_entry.bind('<Return>', lambda e: login())
        username_entry.bind('<Return>', lambda e: password_entry.focus())
    
    def create_widgets(self):
        """Создает элементы интерфейса."""
        # Верхняя панель с авторизацией
        top_frame = tk.Frame(self.root, bg='#2c3e50', relief='flat')
        top_frame.pack(fill='x', padx=0, pady=0)
        
        # Заголовок
        title_label = tk.Label(
            top_frame,
            text="BUCKET SORT - Сортировка массивов",
            font=('Segoe UI', 18, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(side='left', padx=25, pady=15)
        
        # Панель авторизации
        auth_frame = tk.Frame(top_frame, bg='#2c3e50')
        auth_frame.pack(side='right', padx=25, pady=15)
        
        self.auth_status_label = tk.Label(
            auth_frame,
            text="Не авторизован",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        self.auth_status_label.pack(side='left', padx=10)
        
        self.login_button = tk.Button(
            auth_frame,
            text="Войти",
            command=self.show_login_dialog,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        )
        self.login_button.pack(side='left', padx=3)
        
        self.logout_button = tk.Button(
            auth_frame,
            text="Выйти",
            command=self.logout,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=5,
            relief='flat',
            state='disabled',
            cursor='hand2',
            activebackground='#c0392b',
            activeforeground='white'
        )
        self.logout_button.pack(side='left', padx=3)
        
        # Основной контент
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Левая панель - ввод данных
        left_panel = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', padx=(0, 10), expand=False, ipadx=10, ipady=10)
        
        # Заголовок панели ввода
        tk.Label(
            left_panel,
            text="Ввод данных",
            font=('Segoe UI', 14, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15), padx=10)
        
        # Кнопки ввода данных
        input_btn_frame = tk.Frame(left_panel, bg='#ffffff')
        input_btn_frame.pack(fill='x', padx=10, pady=5)
        
        btn_input = tk.Button(
            input_btn_frame,
            text="📝 Ввести массив",
            command=self.input_array,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white',
            width=20
        )
        btn_input.pack(fill='x', pady=5)
        
        btn_generate = tk.Button(
            input_btn_frame,
            text="🎲 Сгенерировать случайный",
            command=self.generate_random,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#8e44ad',
            activeforeground='white',
            width=20
        )
        btn_generate.pack(fill='x', pady=5)
        
        btn_load = tk.Button(
            input_btn_frame,
            text="📂 Загрузить из файла",
            command=self.load_from_file,
            bg='#f39c12',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#e67e22',
            activeforeground='white',
            width=20
        )
        btn_load.pack(fill='x', pady=5)
        
        # Кнопка сортировки
        self.sort_button = tk.Button(
            input_btn_frame,
            text="🔄 Отсортировать",
            command=self.sort_array,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            padx=20,
            pady=12,
            relief='flat',
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white',
            width=20,
            state='disabled'
        )
        self.sort_button.pack(fill='x', pady=(15, 5))
        
        # Кнопки истории
        tk.Label(
            left_panel,
            text="История",
            font=('Segoe UI', 12, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(20, 10), padx=10)
        
        history_btn_frame = tk.Frame(left_panel, bg='#ffffff')
        history_btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.save_button = tk.Button(
            history_btn_frame,
            text="💾 Сохранить результат",
            command=self.save_sort_result,
            bg='#16a085',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            activebackground='#138d75',
            activeforeground='white',
            width=20,
            state='disabled'
        )
        self.save_button.pack(fill='x', pady=5)
        
        self.history_button = tk.Button(
            history_btn_frame,
            text="📋 Просмотр истории",
            command=self.show_history,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2',
            activebackground='#c0392b',
            activeforeground='white',
            width=20,
            state='disabled'
        )
        self.history_button.pack(fill='x', pady=5)
        
        # Правая панель - отображение результатов
        right_panel = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=1)
        right_panel.pack(side='left', fill='both', expand=True, ipadx=10, ipady=10)
        
        # Заголовок панели результатов
        tk.Label(
            right_panel,
            text="Результаты",
            font=('Segoe UI', 14, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10), padx=10)
        
        # Информационная панель
        self.info_label = tk.Label(
            right_panel,
            text="Введите или загрузите массив для начала работы",
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#34495e',
            anchor='w',
            padx=15,
            pady=10,
            relief='flat'
        )
        self.info_label.pack(fill='x', padx=10, pady=(0, 15))
        
        # Исходный массив
        orig_frame = tk.LabelFrame(
            right_panel,
            text="Исходный массив",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg='#2c3e50',
            relief='flat',
            bd=1
        )
        orig_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.original_text = ScrolledText(
            orig_frame,
            font=('Consolas', 11),
            bg='#f8f9fa',
            fg='#2c3e50',
            wrap='word',
            relief='flat',
            padx=10,
            pady=10,
            height=8
        )
        self.original_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.original_text.insert('1.0', "Массив не задан")
        self.original_text.config(state='disabled')
        
        # Отсортированный массив
        sorted_frame = tk.LabelFrame(
            right_panel,
            text="Отсортированный массив",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg='#2c3e50',
            relief='flat',
            bd=1
        )
        sorted_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.sorted_text = ScrolledText(
            sorted_frame,
            font=('Consolas', 11),
            bg='#f8f9fa',
            fg='#27ae60',
            wrap='word',
            relief='flat',
            padx=10,
            pady=10,
            height=8
        )
        self.sorted_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.sorted_text.insert('1.0', "Результат появится после сортировки")
        self.sorted_text.config(state='disabled')
        
        # Нижняя панель с кнопкой помощи
        bottom_frame = tk.Frame(self.root, bg='#ecf0f1')
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        help_button = tk.Button(
            bottom_frame,
            text="❓ Справка",
            command=self.show_help,
            bg='#34495e',
            fg='white',
            font=('Segoe UI', 9),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2',
            activebackground='#2c3e50',
            activeforeground='white'
        )
        help_button.pack(side='right')
    
    def update_auth_status(self):
        """Обновляет статус авторизации в интерфейсе."""
        if self.auth_manager.is_authenticated():
            username = self.auth_manager.get_current_username()
            self.auth_status_label.config(text=f"Пользователь: {username}", fg='#ecf0f1')
            self.login_button.config(state='disabled')
            self.logout_button.config(state='normal')
            self.history_button.config(state='normal')
        else:
            self.auth_status_label.config(text="Не авторизован", fg='#bdc3c7')
            self.login_button.config(state='normal')
            self.logout_button.config(state='disabled')
            self.history_button.config(state='disabled')
    
    def sort_array(self):
        """Выполняет сортировку массива."""
        if not self.original_array:
            messagebox.showwarning("Предупреждение", "Сначала введите или загрузите массив!")
            return
        
        try:
            self.info_label.config(text="Выполняется сортировка...", fg='#3498db')
            self.root.update()
            
            # Выполняем сортировку
            self.sorted_array = bucket_sort(self.original_array.copy())
            
            # Обновляем отображение
            self.original_text.config(state='normal')
            self.original_text.delete('1.0', tk.END)
            self.original_text.insert('1.0', str(self.original_array))
            self.original_text.config(state='disabled')
            
            self.sorted_text.config(state='normal')
            self.sorted_text.delete('1.0', tk.END)
            self.sorted_text.insert('1.0', str(self.sorted_array))
            self.sorted_text.config(state='disabled')
            
            self.info_label.config(
                text=f"Сортировка завершена! Отсортировано {len(self.sorted_array)} элементов",
                fg='#27ae60'
            )
            
            self.save_button.config(state='normal')
            messagebox.showinfo("Успех", "Массив успешно отсортирован!")
        except Exception as e:
            self.info_label.config(text=f"Ошибка при сортировке: {str(e)}", fg='#e74c3c')
            messagebox.showerror("Ошибка", f"Ошибка при сортировке: {str(e)}")
    
    def logout(self):
        """Выполняет выход пользователя."""
        self.auth_manager.logout()
        self.update_auth_status()
        messagebox.showinfo("Выход", "Вы вышли из системы")
    
    def save_sort_result(self):
        """Сохраняет результат сортировки в базу данных."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться для сохранения истории!")
            self.show_login_dialog()
            return
        
        if not self.original_array or self.sorted_array is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните сортировку!")
            return
        
        user_id = self.auth_manager.get_current_user_id()
        success, msg = self.auth_manager.db.save_sort_history(
            user_id,
            self.original_array,
            self.sorted_array
        )
        
        if success:
            messagebox.showinfo("Успех", "Результат сохранен в историю!")
        else:
            messagebox.showerror("Ошибка", msg)
    
    def show_history(self):
        """Показывает историю сортировок пользователя."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться для просмотра истории!")
            self.show_login_dialog()
            return
        
        user_id = self.auth_manager.get_current_user_id()
        history = self.auth_manager.db.get_sort_history(user_id)
        
        if not history:
            messagebox.showinfo("История", "История сортировок пуста")
            return
        
        # Создаем окно истории
        history_window = tk.Toplevel(self.root)
        history_window.title("История сортировок")
        history_window.geometry("850x650")
        history_window.configure(bg='#ecf0f1')
        
        # Центрируем окно
        history_window.update_idletasks()
        x = (history_window.winfo_screenwidth() // 2) - (850 // 2)
        y = (history_window.winfo_screenheight() // 2) - (650 // 2)
        history_window.geometry(f"850x650+{x}+{y}")
        
        # Заголовок
        title_frame = tk.Frame(history_window, bg='#2c3e50')
        title_frame.pack(fill='x')
        tk.Label(
            title_frame,
            text=f"История сортировок ({len(history)} записей)",
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=15)
        
        # Прокручиваемая область
        canvas = tk.Canvas(history_window, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Отображаем историю
        for idx, record in enumerate(history):
            record_frame = tk.Frame(
                scrollable_frame,
                bg='#ffffff',
                relief='flat',
                bd=1
            )
            record_frame.pack(fill='x', padx=15, pady=8)
            
            # Заголовок записи
            header_frame = tk.Frame(record_frame, bg='#34495e', relief='flat')
            header_frame.pack(fill='x')
            tk.Label(
                header_frame,
                text=f"Запись #{len(history) - idx} | {record['created_at']}",
                font=('Segoe UI', 11, 'bold'),
                bg='#34495e',
                fg='#ecf0f1'
            ).pack(anchor='w', padx=15, pady=8)
            
            # Контент записи
            content_frame = tk.Frame(record_frame, bg='#ffffff')
            content_frame.pack(fill='x', padx=10, pady=10)
            
            # Исходный массив
            tk.Label(
                content_frame,
                text="Исходный массив:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#2c3e50',
                anchor='w'
            ).pack(anchor='w', padx=5, pady=(0, 3))
            
            orig_text = str(record['original_array'])
            if len(orig_text) > 100:
                orig_text = f"{str(record['original_array'])[:80]}... ({len(record['original_array'])} элементов)"
            
            orig_label = tk.Label(
                content_frame,
                text=orig_text,
                font=('Consolas', 9),
                bg='#f8f9fa',
                fg='#2c3e50',
                anchor='w',
                wraplength=750,
                justify='left',
                padx=10,
                pady=5
            )
            orig_label.pack(fill='x', padx=5, pady=(0, 10))
            
            # Отсортированный массив
            tk.Label(
                content_frame,
                text="Отсортированный массив:",
                font=('Segoe UI', 10, 'bold'),
                bg='#ffffff',
                fg='#27ae60',
                anchor='w'
            ).pack(anchor='w', padx=5, pady=(0, 3))
            
            sorted_text = str(record['sorted_array'])
            if len(sorted_text) > 100:
                sorted_text = f"{str(record['sorted_array'])[:80]}... ({len(record['sorted_array'])} элементов)"
            
            sorted_label = tk.Label(
                content_frame,
                text=sorted_text,
                font=('Consolas', 9),
                bg='#f8f9fa',
                fg='#27ae60',
                anchor='w',
                wraplength=750,
                justify='left',
                padx=10,
                pady=5
            )
            sorted_label.pack(fill='x', padx=5, pady=(0, 10))
            
            # Кнопка загрузки
            def load_array(orig_arr, sorted_arr):
                self.original_array = orig_arr
                self.sorted_array = sorted_arr
                
                self.original_text.config(state='normal')
                self.original_text.delete('1.0', tk.END)
                self.original_text.insert('1.0', str(orig_arr))
                self.original_text.config(state='disabled')
                
                self.sorted_text.config(state='normal')
                self.sorted_text.delete('1.0', tk.END)
                self.sorted_text.insert('1.0', str(sorted_arr))
                self.sorted_text.config(state='disabled')
                
                self.sort_button.config(state='normal')
                self.save_button.config(state='normal')
                self.info_label.config(text=f"Массив загружен из истории: {len(orig_arr)} элементов", fg='#27ae60')
                history_window.destroy()
                messagebox.showinfo("Успех", "Массив загружен!")
            
            btn_frame = tk.Frame(content_frame, bg='#ffffff')
            btn_frame.pack(fill='x', padx=5, pady=5)
            
            tk.Button(
                btn_frame,
                text="Загрузить",
                command=lambda o=record['original_array'], s=record['sorted_array']: load_array(o, s),
                bg='#27ae60',
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                padx=20,
                pady=6,
                relief='flat',
                cursor='hand2',
                activebackground='#229954',
                activeforeground='white'
            ).pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Плавное появление окна
        history_window.withdraw()
        history_window.deiconify()
        history_window.update()
    
    def show_help(self):
        """Показывает справку по использованию приложения."""
        help_text = """
BUCKET SORT - СПРАВКА

1. АВТОРИЗАЦИЯ:
   - Нажмите "Войти" для входа в систему
   - Используйте "Регистрация" для создания нового аккаунта
   - Авторизация необходима для сохранения истории сортировок

2. ВВОД ДАННЫХ:
   - "📝 Ввести массив" - ввод чисел с клавиатуры через пробел
   - "🎲 Сгенерировать случайный" - автоматическая генерация массива
   - "📂 Загрузить из файла" - загрузка из текстового файла

3. СОРТИРОВКА:
   - "🔄 Отсортировать" - выполнение сортировки массива алгоритмом Bucket Sort
   - Результат отобразится в правой панели

4. СОХРАНЕНИЕ И ИСТОРИЯ:
   - "💾 Сохранить результат" - сохранение результата в историю (требуется авторизация)
   - "📋 Просмотр истории" - просмотр сохраненных сортировок
   - Вы можете загрузить любой массив из истории обратно в приложение

5. АЛГОРИТМ BUCKET SORT:
   - Распределяет элементы по "ведрам" на основе их значений
   - Сортирует каждое ведро отдельно (используется Insertion Sort)
   - Объединяет отсортированные ведра в итоговый массив
   - Временная сложность: O(n) в лучшем случае, O(n²) в худшем случае

МАКСИМАЛЬНЫЙ РАЗМЕР МАССИВА: 1000 элементов
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("650x550")
        help_window.configure(bg='#ecf0f1')
        
        # Центрируем окно
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (help_window.winfo_screenheight() // 2) - (550 // 2)
        help_window.geometry(f"650x550+{x}+{y}")
        
        # Заголовок
        title_frame = tk.Frame(help_window, bg='#2c3e50')
        title_frame.pack(fill='x')
        tk.Label(
            title_frame,
            text="Справка",
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=15)
        
        text_widget = tk.Text(
            help_window,
            wrap='word',
            font=('Segoe UI', 11),
            bg='white',
            fg='#2c3e50',
            padx=20,
            pady=20,
            relief='flat'
        )
        text_widget.pack(fill='both', expand=True, padx=15, pady=15)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        button_frame = tk.Frame(help_window, bg='#ecf0f1')
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Закрыть",
            command=help_window.destroy,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        ).pack()
    
    def input_array(self):
        """Ввод массива с клавиатуры."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Ввод массива")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        
        # Центрируем окно
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"500x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text=f"Введите элементы массива через пробел (максимум {self.MAX_ARRAY_SIZE} элементов):",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wraplength=450
        ).pack(pady=(20, 10), padx=20)
        
        entry = tk.Entry(
            dialog,
            font=('Consolas', 12),
            width=50,
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        entry.pack(pady=10, padx=20, fill='x')
        entry.focus()
        
        def ok():
            try:
                arr = [int(x) for x in entry.get().strip().split()]
                if not arr:
                    messagebox.showerror("Ошибка", "Массив не может быть пустым!")
                elif len(arr) > self.MAX_ARRAY_SIZE:
                    messagebox.showerror(
                        "Ошибка",
                        f"Размер массива превышает максимально допустимый!\n"
                        f"Максимум: {self.MAX_ARRAY_SIZE} элементов\n"
                        f"Введено: {len(arr)} элементов"
                    )
                else:
                    self.original_array = arr
                    self.sorted_array = None
                    self.original_text.config(state='normal')
                    self.original_text.delete('1.0', tk.END)
                    self.original_text.insert('1.0', str(arr))
                    self.original_text.config(state='disabled')
                    
                    self.sorted_text.config(state='normal')
                    self.sorted_text.delete('1.0', tk.END)
                    self.sorted_text.insert('1.0', "Результат появится после сортировки")
                    self.sorted_text.config(state='disabled')
                    
                    self.sort_button.config(state='normal')
                    self.save_button.config(state='disabled')
                    self.info_label.config(text=f"Массив загружен: {len(arr)} элементов", fg='#27ae60')
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите только целые числа!")
        
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="OK",
            command=ok,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=8,
            relief='flat',
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        ).pack()
        
        entry.bind('<Return>', lambda e: ok())
    
    def generate_random(self):
        """Генерация случайного массива."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Генерация массива")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        
        # Центрируем окно
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"500x350+{x}+{y}")
        
        # Заголовок
        title_frame = tk.Frame(dialog, bg='#2c3e50')
        title_frame.pack(fill='x')
        tk.Label(
            title_frame,
            text="Генерация случайного массива",
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=15)
        
        # Контейнер для полей ввода
        content_frame = tk.Frame(dialog, bg='#ecf0f1')
        content_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        # Размер массива
        size_frame = tk.Frame(content_frame, bg='#ecf0f1')
        size_frame.pack(fill='x', pady=10)
        tk.Label(
            size_frame,
            text=f"Размер массива (1-{self.MAX_ARRAY_SIZE}):",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(side='left', padx=5)
        size_entry = tk.Entry(
            size_frame,
            font=('Consolas', 12),
            width=20,
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        size_entry.pack(side='left', padx=5)
        size_entry.insert(0, "20")
        
        # Минимальное значение
        min_frame = tk.Frame(content_frame, bg='#ecf0f1')
        min_frame.pack(fill='x', pady=10)
        tk.Label(
            min_frame,
            text="Минимальное значение:",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(side='left', padx=5)
        min_entry = tk.Entry(
            min_frame,
            font=('Consolas', 12),
            width=20,
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        min_entry.pack(side='left', padx=5)
        min_entry.insert(0, "1")
        
        # Максимальное значение
        max_frame = tk.Frame(content_frame, bg='#ecf0f1')
        max_frame.pack(fill='x', pady=10)
        tk.Label(
            max_frame,
            text="Максимальное значение:",
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(side='left', padx=5)
        max_entry = tk.Entry(
            max_frame,
            font=('Consolas', 12),
            width=20,
            relief='flat',
            bd=5,
            bg='white',
            fg='#2c3e50'
        )
        max_entry.pack(side='left', padx=5)
        max_entry.insert(0, "100")
        
        # Label для отображения ошибок валидации
        validation_label = tk.Label(
            content_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#e74c3c',
            wraplength=450
        )
        validation_label.pack(pady=10)
        
        def validate_inputs():
            """Проверяет корректность введенных значений."""
            try:
                size = int(size_entry.get())
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                
                errors = []
                
                if size <= 0:
                    errors.append("Размер массива должен быть положительным числом!")
                elif size > self.MAX_ARRAY_SIZE:
                    errors.append(f"Размер массива не должен превышать {self.MAX_ARRAY_SIZE}!")
                
                if min_val > max_val:
                    errors.append("Минимальное значение не может быть больше максимального!")
                
                if min_val > 1000000 or max_val > 1000000:
                    errors.append("Значения не должны превышать 1,000,000!")
                
                if min_val < -1000000 or max_val < -1000000:
                    errors.append("Значения не должны быть меньше -1,000,000!")
                
                if errors:
                    validation_label.config(text="\n".join(errors))
                    return False
                else:
                    validation_label.config(text="")
                    return True
                
            except ValueError:
                validation_label.config(text="Все поля должны содержать целые числа!")
                return False
        
        def generate():
            if validate_inputs():
                try:
                    size = int(size_entry.get())
                    min_val = int(min_entry.get())
                    max_val = int(max_entry.get())
                    
                    self.original_array = [random.randint(min_val, max_val) for _ in range(size)]
                    self.sorted_array = None
                    
                    self.original_text.config(state='normal')
                    self.original_text.delete('1.0', tk.END)
                    self.original_text.insert('1.0', str(self.original_array))
                    self.original_text.config(state='disabled')
                    
                    self.sorted_text.config(state='normal')
                    self.sorted_text.delete('1.0', tk.END)
                    self.sorted_text.insert('1.0', "Результат появится после сортировки")
                    self.sorted_text.config(state='disabled')
                    
                    self.sort_button.config(state='normal')
                    self.save_button.config(state='disabled')
                    self.info_label.config(text=f"Сгенерирован массив из {size} элементов", fg='#27ae60')
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при генерации: {e}")
        
        # Кнопки
        button_frame = tk.Frame(content_frame, bg='#ecf0f1')
        button_frame.pack(pady=5)
        
        generate_button = tk.Button(
            button_frame,
            text="Сгенерировать",
            command=generate,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#8e44ad',
            activeforeground='white'
        )
        generate_button.pack(side='left', padx=5)
        
        cancel_button = tk.Button(
            button_frame,
            text="Отмена",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 12),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2',
            activebackground='#7f8c8d',
            activeforeground='white'
        )
        cancel_button.pack(side='left', padx=5)
        
        # Валидация при вводе
        def on_entry_change(*args):
            validate_inputs()
        
        size_entry.bind('<KeyRelease>', on_entry_change)
        min_entry.bind('<KeyRelease>', on_entry_change)
        max_entry.bind('<KeyRelease>', on_entry_change)
        
        # Фокус на первом поле и обработка Enter
        size_entry.focus()
        size_entry.bind('<Return>', lambda e: min_entry.focus())
        min_entry.bind('<Return>', lambda e: max_entry.focus())
        max_entry.bind('<Return>', lambda e: generate())
    
    def load_from_file(self):
        """Загрузка массива из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    numbers = []
                    for line in content.split('\n'):
                        numbers.extend([int(x) for x in line.split() if x.strip()])
                    if not numbers:
                        messagebox.showerror("Ошибка", "Файл не содержит чисел!")
                    elif len(numbers) > self.MAX_ARRAY_SIZE:
                        messagebox.showerror(
                            "Ошибка",
                            f"Размер массива в файле превышает максимально допустимый!\n"
                            f"Максимум: {self.MAX_ARRAY_SIZE} элементов\n"
                            f"В файле: {len(numbers)} элементов"
                        )
                    else:
                        self.original_array = numbers
                        self.sorted_array = None
                        
                        self.original_text.config(state='normal')
                        self.original_text.delete('1.0', tk.END)
                        self.original_text.insert('1.0', str(numbers))
                        self.original_text.config(state='disabled')
                        
                        self.sorted_text.config(state='normal')
                        self.sorted_text.delete('1.0', tk.END)
                        self.sorted_text.insert('1.0', "Результат появится после сортировки")
                        self.sorted_text.config(state='disabled')
                        
                        self.sort_button.config(state='normal')
                        self.save_button.config(state='disabled')
                        self.info_label.config(text=f"Загружено {len(numbers)} элементов из файла", fg='#27ae60')
            except ValueError:
                messagebox.showerror("Ошибка", "Файл должен содержать только целые числа!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке файла: {e}")
    


def main():
    """Главная функция для запуска приложения."""
    root = tk.Tk()
    app = BucketSortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()