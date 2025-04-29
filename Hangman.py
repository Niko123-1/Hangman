import random
from PIL import Image, ImageTk
from tkinter import Label, Button, Frame, messagebox, Canvas

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Виселица")

        # Инициализируем атрибуты
        self.hangman_images = []
        self.current_hangman_stage = 0
        self.difficulty = None
        self.secret_word = ""
        self.guessed_letters = set()
        self.letter_buttons = {}  # Словарь для хранения кнопок букв

        # Загружаем изображения
        self.load_hangman_images()

        # Создаем Label для картинки (но пока не отображаем)
        self.image_label = Label(self.root)

        # Начинаем с выбора сложности
        self.setup_difficulty_ui()

    def load_hangman_images(self):
        """Загружает все изображения виселицы"""
        try:
            for i in range(0, 6):  # 5 стадий виселицы (Hang_1.png до Hang_5.png)
                image = Image.open(f"Hang_{i}.png")
                photo = ImageTk.PhotoImage(image)
                self.hangman_images.append(photo)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Не найдены файлы с изображениями виселицы!")
            self.root.destroy()

    def setup_difficulty_ui(self):
        """Создаёт интерфейс выбора сложности."""
        self.clear_window()

        # Сбрасываем и прячем изображение
        self.image_label.config(image='')
        self.image_label.pack_forget()
        self.current_hangman_stage = 0

        label = Label(self.root, text="Выберите уровень сложности:", font=("Arial", 14))
        label.pack(pady=10)

        Button(self.root, text="Лёгкий", command=lambda: self.start_game(1)).pack(pady=20)
        Button(self.root, text="Средний", command=lambda: self.start_game(2)).pack(pady=20)
        Button(self.root, text="Сложный", command=lambda: self.start_game(3)).pack(pady=20)

    def start_game(self, difficulty):
        """Начинает игру с выбранной сложностью."""
        self.difficulty = difficulty
        self.secret_word = self.get_random_word(difficulty).upper()
        self.guessed_letters = set()
        self.current_hangman_stage = 0
        self.letter_buttons = {}

        if not self.secret_word:
            messagebox.showerror("Ошибка", "Нет слов подходящей длины в файле!")
            return

        # Отображаем изображение (первую стадию)
        self.update_hangman_image()
        self.image_label.pack()  # Показываем изображение

        # Открываем подсказки в зависимости от сложности
        self.reveal_hints()
        self.show_word_display()

    def reveal_hints(self):
        """Открывает подсказки в зависимости от сложности."""
        if self.difficulty == 2 or self.difficulty == 1:
            # Открываем 1 случайную букву
            closed_positions = [i for i, char in enumerate(self.secret_word) if char not in self.guessed_letters]
            if closed_positions:
                pos = random.choice(closed_positions)
                self.guessed_letters.add(self.secret_word[pos])
        elif self.difficulty == 3:
            # Открываем 2 разные буквы
            unique_chars = list(set(self.secret_word) - self.guessed_letters)
            if len(unique_chars) >= 2:
                for char in random.sample(unique_chars, 2):
                    self.guessed_letters.add(char)
            elif unique_chars:
                self.guessed_letters.add(unique_chars[0])

    def show_word_display(self):
        """Показывает загаданное слово."""
        self.clear_window()

        # Убедимся, что изображение видно
        self.image_label.pack()

        # Показываем слово с угаданными буквами
        display_word = " ".join([char if char in self.guessed_letters else "_" for char in self.secret_word])
        Label(self.root, text=display_word, font=("Arial", 24)).pack(pady=20)
        Label(self.root, text=f"Слово из {len(self.secret_word)} букв", font=("Arial", 12)).pack()

        # Кнопка для начала заново
        Button(self.root, text="Начать заново", command=self.setup_difficulty_ui).pack(side="bottom", pady=10)

        # Создаем клавиатуру
        self.create_keyboard()

        # Делаем неактивными уже угаданные буквы
        self.update_keyboard_state()

    def create_keyboard(self):
        """Создает виртуальную клавиатуру с русскими буквами."""
        russian_letters = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И',
            'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
            'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь',
            'Э', 'Ю', 'Я'
        ]

        keyboard_frame = Frame(self.root)
        keyboard_frame.pack(pady=10)

        for i, letter in enumerate(russian_letters):
            btn = Button(
                keyboard_frame,
                text=letter,
                font=("Arial", 12),
                width=3,
                command=lambda l=letter: self.guess_letter(l)
            )
            btn.grid(row=i // 10, column=i % 10, padx=2, pady=2)
            self.letter_buttons[letter] = btn  # Сохраняем ссылку на кнопку

    def update_keyboard_state(self):
        """Обновляет состояние кнопок клавиатуры."""
        for letter, btn in self.letter_buttons.items():
            if letter in self.guessed_letters:
                btn.config(state="disabled")
                # Рисуем крестик на кнопке
                canvas = Canvas(btn, width=20, height=20, highlightthickness=0)
                canvas.create_line(2, 2, 18, 18, width=2, fill="red")
                canvas.create_line(2, 18, 18, 2, width=2, fill="red")
                canvas.place(relx=0.5, rely=0.5, anchor="center")
                btn.config(text="")  # Убираем текст буквы

    def guess_letter(self, letter):
        """Обрабатывает угадывание буквы."""
        # Если буква уже угадана или игра закончена - ничего не делаем
        if letter in self.guessed_letters or self.current_hangman_stage >= len(self.hangman_images) - 1:
            return

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            # Обновляем состояние клавиатуры
            self.update_keyboard_state()

            # Проверяем, угадано ли всё слово
            if all(char in self.guessed_letters for char in self.secret_word):
                messagebox.showinfo("Победа!", f"Вы выиграли! Слово: {self.secret_word}")
                self.setup_difficulty_ui()
            else:
                self.show_word_display()
        else:
            self.current_hangman_stage += 1
            self.update_hangman_image()
            self.update_keyboard_state()

            # Если это была последняя попытка
            if self.current_hangman_stage >= len(self.hangman_images) - 1:
                self.disable_keyboard()
                messagebox.showinfo("Поражение", f"Игра окончена! Слово было: {self.secret_word}")

    def disable_keyboard(self):
        """Блокирует всю клавиатуру."""
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")

    def update_hangman_image(self):
        """Обновляет изображение виселицы."""
        if self.hangman_images:
            stage = min(self.current_hangman_stage, len(self.hangman_images) - 1)
            self.image_label.config(image=self.hangman_images[stage])
            self.image_label.image = self.hangman_images[stage]

    def clear_window(self):
        """Очищает окно от всех виджетов, кроме image_label."""
        for widget in self.root.winfo_children():
            if widget != self.image_label:  # Не удаляем label с изображением
                widget.destroy()

    def get_random_word(self, difficulty):
        """Выбирает случайное слово в зависимости от сложности."""
        try:
            with open('Words.txt', 'r', encoding='utf-8') as f:
                words = [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Words.txt не найден!")
            return None

        if difficulty == 1:
            filtered_words = [word for word in words if len(word) <= 4]
        elif difficulty == 2:
            filtered_words = [word for word in words if 5 <= len(word) <= 7]
        elif difficulty == 3:
            filtered_words = [word for word in words if len(word) > 7]

        return random.choice(filtered_words) if filtered_words else None