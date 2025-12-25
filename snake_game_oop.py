

import msvcrt
import os
import sys
import time
import random
import pickle
from datetime import datetime


if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.system('chcp 65001 >nul 2>&1')




class Position:
    """Клас для представлення позиції на полі"""
    
    def __init__(self, x, y):
        """
        Конструктор позиції
        
        Args:
            x: Координата X
            y: Координата Y
        """
        self.__x = x  # Приватний атрибут
        self.__y = y  # Приватний атрибут
    
    @property
    def x(self):
        """Getter для X"""
        return self.__x
    
    @property
    def y(self):
        """Getter для Y"""
        return self.__y
    
    def __eq__(self, other):
        """Порівняння позицій"""
        if isinstance(other, Position):
            return self.__x == other.__x and self.__y == other.__y
        elif isinstance(other, tuple):
            return self.__x == other[0] and self.__y == other[1]
        return False
    
    def __hash__(self):
        """Хеш для використання в множинах"""
        return hash((self.__x, self.__y))
    
    def __str__(self):
        """Строкове представлення"""
        return f"({self.__x}, {self.__y})"
    
    def __repr__(self):
        """Формальне представлення"""
        return f"Position({self.__x}, {self.__y})"
    
    def to_tuple(self):
        """Конвертує в кортеж"""
        return (self.__x, self.__y)
    
    def move(self, direction):
        """Повертає нову позицію після руху"""
        moves = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        dx, dy = moves.get(direction, (0, 0))
        return Position(self.__x + dx, self.__y + dy)


class Food:
    """Базовий клас для їжі"""
    
    def __init__(self, position):
        """
        Конструктор їжі
        
        Args:
            position: Об'єкт Position або кортеж (x, y)
        """
        if isinstance(position, tuple):
            self._position = Position(position[0], position[1])
        else:
            self._position = position
        
        self._points = 10  # Захищений атрибут
        self._symbol = '*'
    
    @property
    def position(self):
        """Getter для позиції"""
        return self._position
    
    @property
    def points(self):
        """Getter для балів"""
        return self._points
    
    @property
    def symbol(self):
        """Getter для символу"""
        return self._symbol
    
    def __str__(self):
        """Строкове представлення"""
        return f"Food at {self._position} ({self._points} points)"
    
    def __repr__(self):
        """Формальне представлення"""
        return f"Food(position={repr(self._position)}, points={self._points})"



class NormalFood(Food):
    """Звичайна їжа (спадкує від Food)"""
    
    def __init__(self, position):
        """Конструктор звичайної їжі"""
        super().__init__(position)
        self._points = 10
        self._symbol = '*'
    
    def __str__(self):
        """Розширене представлення"""
        return f"NormalFood at {self._position} (+{self._points})"


class BonusFood(Food):
    """Бонусна їжа (спадкує від Food)"""
    
    def __init__(self, position):
        """Конструктор бонусної їжі"""
        super().__init__(position)
        self._points = 25
        self._symbol = '$'
    
    def __str__(self):
        """Розширене представлення"""
        return f"BonusFood at {self._position} (+{self._points})"


class Snake:
    """Клас для змійки"""
    
    def __init__(self, initial_positions):
        """
        Конструктор змійки
        
        Args:
            initial_positions: Список початкових позицій [(x, y), ...]
        """
        # Конвертуємо кортежі в Position об'єкти
        self.__body = []
        for pos in initial_positions:
            if isinstance(pos, tuple):
                self.__body.append(Position(pos[0], pos[1]))
            else:
                self.__body.append(pos)
        self._direction = 'RIGHT'  # Захищений атрибут
        self._visited_cells =set()  # Множина відвіданих клітинок
    
    @property
    def head(self):
        """Getter для голови змійки"""
        return self.__body[0]
    
    @property
    def body(self):
        """Getter для тіла змійки (повертає копію)"""
        return self.__body[:]
    
    @property
    def direction(self):
        """Getter для напрямку"""
        return self._direction
    
    @direction.setter
    def direction(self, value):
        """Setter для напрямку з перевіркою"""
        opposites = {
            'UP': 'DOWN', 'DOWN': 'UP',
            'LEFT': 'RIGHT', 'RIGHT': 'LEFT'
        }
        # Не дозволяємо рухатись у протилежний бік
        if opposites.get(self._direction) != value:
            self._direction = value
    
    def __len__(self):
        """Повертає довжину змійки"""
        return len(self.__body)
    
    def __str__(self):
        """Строкове представлення"""
        return f"Snake(length={len(self.__body)}, head={self.head})"
    
    def __repr__(self):
        """Формальне представлення"""
        return f"Snake(positions={len(self.__body)}, dir='{self._direction}')"
    
    def __contains__(self, position):
        """Перевірка чи позиція є частиною змійки"""
        return position in self.__body
    
    def move(self, grow=False):
        """
        Рухає змій

ку вперед
        
        Args:
            grow: Чи змійка росте (їжа з'їдена)
        """
        new_head = self.head.move(self._direction)
        self.__body.insert(0, new_head)
        self._visited_cells.add((new_head.x, new_head.y))
        
        if not grow:
            self.__body.pop()  # Видаляємо хвіст
    
    def check_collision(self):
        """Перевіряє чи змійка з'їла сама себе"""
        return self.head in self.__body[1:]
    
    def get_visited_count(self):
        """Повертає кількість відвіданих клітинок"""
        return len(self._visited_cells)


class GameField:
    """Клас для ігрового поля"""
    
    def __init__(self, width, height, obstacles=None):
        """
        Конструктор ігрового поля
        
        Args:
            width: Ширина поля
            height: Висота поля
            obstacles: Матриця перешкод
        """
        self._width = width
        self._height = height
        
        # Символи (визначаємо ПЕРЕД викликом _create_empty_matrix)
        self._symbols = {
            'head': 'O',
            'body': 'o',
            'wall': '#',
            'empty': ' '
        }
        
        # Тепер можемо викликати метод, який використовує _symbols
        self.__obstacles = obstacles if obstacles else self._create_empty_matrix()
    
    @property
    def width(self):
        """Getter для ширини"""
        return self._width
    
    @property
    def height(self):
        """Getter для висоти"""
        return self._height
    
    def _create_empty_matrix(self):
        """Створює порожню матрицю з стінами (list comprehension)"""
        matrix = [
            [self._symbols['wall'] if x == 0 or x == self._width-1 or y == 0 or y == self._height-1
             else self._symbols['empty']
             for x in range(self._width)]
            for y in range(self._height)
        ]
        return matrix
    
    def is_obstacle(self, position):
        """Перевіряє чи є перешкода на позиції"""
        x, y = position.x, position.y
        
        if y < 0 or y >= self._height or x < 0 or x >= self._width:
            return True
        
        return self.__obstacles[y][x] == self._symbols['wall']
    
    def get_free_cells(self, snake):
        """Повертає список вільних клітинок (list comprehension)"""
        free_cells = [
            (x, y)
            for y in range(1, self._height-1)
            for x in range(1, self._width-1)
            if self.__obstacles[y][x] == self._symbols['empty'] 
               and Position(x, y) not in snake
        ]
        return free_cells
    
    def draw(self, snake, food):
        """Малює поле на екрані"""
        os.system('cls')
        
        # Створюємо копію матриці для відображення
        display = [row[:] for row in self.__obstacles]
        
        # Розміщуємо їжу
        fx, fy = food.position.x, food.position.y
        display[fy][fx] = food.symbol
        
        # Розміщуємо змійку
        for i, pos in enumerate(snake.body):
            symbol = self._symbols['head'] if i == 0 else self._symbols['body']
            display[pos.y][pos.x] = symbol
        
        # Малюємо
        for row in display:
            print(''.join(row))


class GameState:
    """Клас для стану гри"""
    
    def __init__(self):
        """Конструктор стану гри"""
        self.__score = 0  # Приватний атрибут
        self.__high_score = 0
        self._speed = 0.2  # Захищений атрибут
        self._level = 1
    
    @property
    def score(self):
        """Getter для рахунку"""
        return self.__score
    
    @score.setter
    def score(self, value):
        """Setter для рахунку"""
        self.__score = value
        if self.__score > self.__high_score:
            self.__high_score = self.__score
    
    @property
    def high_score(self):
        """Getter для рекорду"""
        return self.__high_score
    
    @property
    def speed(self):
        """Getter для швидкості"""
        return self._speed
    
    @property
    def level(self):
        """Getter для рівня"""
        return self._level
    
    def add_points(self, points):
        """Додає бали"""
        self.__score += points
        if self.__score > self.__high_score:
            self.__high_score = self.__score
    
    def make_faster(self):
        """Прискорює гру"""
        self._speed = max(0.05, self._speed - 0.02)
    
    def reset(self, level=1):
        """Скидає стан гри"""
        self.__score = 0
        self._speed = 0.2
        self._level = level
    
    def __str__(self):
        """Строкове представлення"""
        return f"Score: {self.__score} | Record: {self.__high_score} | Level: {self._level}"
    
    def __add__(self, points):
        """Додавання балів через оператор +"""
        self.add_points(points)
        return self




class SnakeGame:
    """Головний клас гри"""
    
    def __init__(self):
        """Конструктор гри"""
        self._state = GameState()
        self._field = None
        self._snake = None
        self._food = None
        self._levels = self._load_levels()  # Завантажуємо рівні
        print(f"[DEBUG] Завантажено рівнів: {len(self._levels)}")  # Debug
    
    def start(self):
        """Запускає гру"""
        print("=" * 40)
        print("         ГРА ЗМІЙКА 3.0 (OOP)")
        print("=" * 40)
        print("\n1. Нова гра")
        print("2. Завантажити гру")
        print("3. Рекорди")
        print("4. Вихід\n")
        
        choice = input("Вибери опцію (1-4): ")
        
        if choice == '1':
            self._select_level()
        elif choice == '2':
            self._load_game()
        elif choice == '3':
            self._show_highscores()
            input("\nНатисни Enter...")
            self.start()
        elif choice == '4':
            print("До побачення!")
        else:
            self.start()
    
    def _select_level(self):
        """Вибір рівня"""
        print("\n" + "=" * 40)
        print(f"Доступно рівнів: {len(self._levels)}")
        
        for i in range(len(self._levels)):
            print(f"{i + 1}. Рівень {i + 1}")
        
        choice = input("\nВибери рівень: ")
        
        try:
            level_num = int(choice) - 1
            if 0 <= level_num < len(self._levels):
                self._new_game(self._levels[level_num], level_num + 1)
            else:
                print("Невірний рівень!")
                self._select_level()
        except ValueError:
            self._select_level()
    
    def _new_game(self, level_data=None, level_num=1):
        """Починає нову гру"""
        # Якщо рівень не вказано, використовуємо дефолтний
        if level_data is None:
            width, height, obstacles = 15, 10, None
        else:
            width, height, obstacles = level_data
        
        # Створюємо об'єкти
        self._field = GameField(width, height, obstacles)
        self._snake = Snake([(width // 2, height // 2), 
                            (width // 2 - 1, height // 2), 
                            (width // 2 - 2, height // 2)])
        self._state.reset(level_num)
        
        # Генеруємо їжу
        self._spawn_food()
        
        # Запускаємо цикл гри
        self._game_loop()
    
    def _spawn_food(self):
        """Генерує їжу на вільній клітинці"""
        free_cells = self._field.get_free_cells(self._snake)
        
        if free_cells:
            pos = random.choice(free_cells)
            # 20% шанс бонусної їжі
            if random.random() < 0.2:
                self._food = BonusFood(pos)
            else:
                self._food = NormalFood(pos)
    
    def _game_loop(self):
        """Основний ігровий цикл"""
        running = True
        
        while running:
            # Малюємо
            self._field.draw(self._snake, self._food)
            print(self._state)
            print(f"Довжина змійки: {len(self._snake)}")
            print(f"Відвідано клітинок: {self._snake.get_visited_count()}")
            print(f"Поточна їжа: {self._food}")
            print("\nS - Зберегти | Q - Вихід")
            
            # Обробка вводу
            new_dir = self._input_key()
            
            if new_dir == 'QUIT':
                break
            elif new_dir == 'SAVE':
                self._save_game()
                print("Гру збережено!")
                time.sleep(1)
                continue
            elif new_dir:
                self._snake.direction = new_dir
            
            # Рух змійки
            self._snake.move()
            
            # Перевірка зіткнень
            if self._field.is_obstacle(self._snake.head) or self._snake.check_collision():
                print("\n💥 Game Over!")
                print(f"\nТвій рахунок: {self._state.score}")
                print(f"Рекорд: {self._state.high_score}")
                print(f"Відвідано клітинок: {self._snake.get_visited_count()}")
                self._save_highscore()
                break
            
            # Перевірка їжі
            if self._snake.head == self._food.position:
                # Додаємо бали (використання __add__)
                self._state = self._state + self._food.points
                self._state.make_faster()
                
                # Змійка росте
                self._snake.move(grow=True)
                
                # Нова їжа
                self._spawn_food()
            
            time.sleep(self._state.speed)
    
    def _input_key(self):
        """Читає введення з клавіатури"""
        if msvcrt.kbhit():
            key = msvcrt.getch()
            
            if key == b'\xe0':
                key = msvcrt.getch()
                direction_map = {
                    b'H': 'UP',
                    b'P': 'DOWN',
                    b'K': 'LEFT',
                    b'M': 'RIGHT'
                }
                return direction_map.get(key)
            elif key.lower() == b'q':
                return 'QUIT'
            elif key.lower() == b's':
                return 'SAVE'
        
        return None
    
    def _save_game(self):
        """Зберігає гру (демонстрація pickle)"""
        save_data = {
            'snake_body': [(pos.x, pos.y) for pos in self._snake.body],
            'snake_direction': self._snake.direction,
            'food_pos': (self._food.position.x, self._food.position.y),
            'food_type': type(self._food).__name__,
            'state': {
                'score': self._state.score,
                'high_score': self._state.high_score,
                'speed': self._state.speed,
                'level': self._state.level
            }
        }
        
        with open('save_oop.dat', 'wb') as f:
            pickle.dump(save_data, f)
    
    def _load_game(self):
        """Завантажує збережену гру"""
        try:
            with open('save_oop.dat', 'rb') as f:
                save_data = pickle.load(f)
            
            print("Гру завантажено!")
            time.sleep(1)
            
            # Відновлюємо об'єкти
            self._field = GameField(15, 10)
            self._snake = Snake(save_data['snake_body'])
            self._snake._direction = save_data['snake_direction']
            
            # Відновлюємо їжу
            if save_data['food_type'] == 'BonusFood':
                self._food = BonusFood(save_data['food_pos'])
            else:
                self._food = NormalFood(save_data['food_pos'])
            
            # Відновлюємо стан
            self._state = GameState()
            self._state._GameState__score = save_data['state']['score']
            self._state._GameState__high_score = save_data['state']['high_score']
            self._state._speed = save_data['state']['speed']
            self._state._level = save_data['state']['level']
            
            self._game_loop()
            
        except FileNotFoundError:
            print("Збережена гра не знайдена!")
            time.sleep(1)
            self.start()
    
    def _save_highscore(self):
        """Зберігає рекорд у файл"""
        if self._state.score == 0:
            return
        
        name = input("\nВведи своє ім'я: ").strip() or "Гравець"
        date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open('highscores.txt', 'a', encoding='utf-8') as f:
                f.write(f"{self._state.score}|{name}|{date}\n")
            print("Рекорд збережено!")
        except Exception as e:
            print(f"Помилка: {e}")
    
    def _load_levels(self):
        """
        Завантажує рівні з файлу levels.txt
        Демонструє: читання файлів, кортежі, list comprehension
        """
        levels = []
        
        try:
            with open('levels.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Розділяємо файл на блоки (рівні) за подвійним переносом рядка
            blocks = content.split('\n\n')
            
            for block in blocks:
                lines = block.strip().split('\n')
                
                # Пропускаємо пусті блоки
                if not lines or not lines[0].strip():
                    continue
                
                # Пропускаємо блоки-коментарі
                if lines[0].strip().startswith('#'):
                    continue
                
                try:
                    # Перший рядок - розміри (ширина висота)
                    parts = lines[0].split()
                    if len(parts) != 2:
                        continue
                    
                    w, h = int(parts[0]), int(parts[1])
                    
                    # Решта рядків - матриця поля
                    matrix = []
                    for i in range(1, min(len(lines), h + 1)):
                        row = list(lines[i])
                        # Доповнюємо рядок пробілами до потрібної ширини
                        while len(row) < w:
                            row.append(' ')
                        # Обрізаємо до потрібної ширини
                        matrix.append(row[:w])
                    
                    # Додаємо рівень тільки якщо матриця повна
                    if len(matrix) == h:
                        levels.append((w, h, matrix))
                        print(f"[DEBUG] Завантажено рівень: {w}x{h}")
                    else:
                        print(f"[DEBUG] Пропущено неповний рівень: {len(matrix)}/{h}")
                        
                except (ValueError, IndexError) as e:
                    print(f"[DEBUG] Помилка парсингу блоку: {e}")
                    continue
            
        except FileNotFoundError:
            print("[DEBUG] Файл levels.txt не знайдено, використовуємо дефолтні рівні")
            levels = self._create_default_levels()
        
        return levels
    
    def _create_default_levels(self):
        """Створює дефолтні рівні"""
        levels = []
        
        # Рівень 1: Простий (15x10)
        levels.append((15, 10, None))
        
        # Рівень 2: З перешкодами (20x15)
        matrix = self._create_level_with_obstacles(20, 15, [(10, 7), (10, 8)])
        levels.append((20, 15, matrix))
        
        # Рівень 3: Більше перешкод (25x15)
        matrix = self._create_level_with_obstacles(25, 15, 
                                                   [(12, 5), (12, 6), (12, 7), (12, 8), (12, 9)])
        levels.append((25, 15, matrix))
        
        return levels
    
    def _create_level_with_obstacles(self, width, height, obstacle_positions):
        """Створює матрицю рівня з перешкодами"""
        # Створюємо порожню матрицю
        matrix = [
            ['#' if x == 0 or x == width-1 or y == 0 or y == height-1 
             else ' '
             for x in range(width)]
            for y in range(height)
        ]
        
        # Додаємо перешкоди
        for x, y in obstacle_positions:
            if 0 < x < width-1 and 0 < y < height-1:
                matrix[y][x] = '#'
        
        return matrix
    

    
    def _show_highscores(self):
        """Показує таблицю рекордів"""
        print("\n" + "=" * 40)
        print("         ТОП-5 РЕКОРДІВ")
        print("=" * 40)
        
        try:
            with open('highscores.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            scores = []
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    score, name, date = parts
                    scores.append((int(score), name, date))
            
            scores.sort(reverse=True)
            top_scores = scores[:5]  # Зріз
            
            for i, (score, name, date) in enumerate(top_scores, 1):
                print(f"{i}. {name}: {score} балів ({date})")
            
        except FileNotFoundError:
            print("Рекордів поки немає")




def main():
    """Головна функція"""
    game = SnakeGame()
    game.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nВихід!")
