"""
Гра Змійка - Лабораторна 2
Розширена версія з матрицями, словниками та файлами
"""

import msvcrt
import os
import time
import random
import pickle
from datetime import datetime

# Глобальні змінні
game_state = {
    'score': 0,
    'high_score': 0,
    'speed': 0.2,
    'level': 1,
    'visited_cells': set()  # Множина відвіданих клітинок
}

# Словник налаштувань
config = {
    'width': 15,
    'height': 10,
    'symbols': {
        'head': 'O',
        'body': 'o',
        'food': '*',
        'wall': '#',
        'bonus': '$',
        'empty': ' '
    },
    'food_types': {
        'normal': {'points': 10, 'symbol': '*'},
        'bonus': {'points': 25, 'symbol': '$'}
    }
}


def main():
    """Головна функція"""
    print("=" * 40)
    print("         ГРА ЗМІЙКА 2.0")
    print("=" * 40)
    print("\n1. Нова гра")
    print("2. Завантажити гру")
    print("3. Рекорди")
    print("4. Вихід\n")
    
    choice = input("Вибери опцію (1-4): ")
    
    if choice == '1':
        select_level()
    elif choice == '2':
        load_game()
    elif choice == '3':
        show_highscores()
        input("\nНатисни Enter...")
        main()
    elif choice == '4':
        print("До побачення!")
    else:
        main()


def select_level():
    """Вибір рівня"""
    levels = load_levels()
    
    print("\n" + "=" * 40)
    print(f"Доступно рівнів: {len(levels)}")
    
    for i in range(len(levels)):
        print(f"{i + 1}. Рівень {i + 1}")
    
    choice = input("\nВибери рівень: ")
    
    try:
        level_num = int(choice) - 1
        if 0 <= level_num < len(levels):
            game_loop(levels[level_num], level_num + 1)
        else:
            print("Невірний рівень!")
            select_level()
    except ValueError:
        select_level()


def load_levels():
    """
    Завантажує рівні з текстового файлу.
    Демонструє: читання файлів, список списків (матриця), кортежі
    """
    levels = []
    
    try:
        with open('levels.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Розділяємо на рівні
        level_blocks = content.strip().split('\n\n')
        
        for block in level_blocks:
            lines = block.strip().split('\n')
            
            if lines[0].startswith('#'):
                continue
            
            # Перший рядок - розміри
            w, h = map(int, lines[0].split())
            
            # Створюємо матрицю поля
            matrix = []
            for i in range(1, len(lines)):
                if lines[i]:
                    row = list(lines[i])
                    matrix.append(row)
            
            # Зберігаємо як кортеж (незмінний)
            levels.append((w, h, matrix))
        
    except FileNotFoundError:
        # Якщо файлу немає, створюємо дефолтний рівень
        w, h = 15, 10
        matrix = create_empty_matrix(w, h)
        levels.append((w, h, matrix))
    
    return levels


def create_empty_matrix(w, h):
    """
    Створює порожню матрицю з стінами.
    Демонструє: list comprehension, матриці
    """
    # List comprehension для створення матриці
    matrix = [
        [config['symbols']['wall'] if x == 0 or x == w-1 or y == 0 or y == h-1 
         else config['symbols']['empty']
         for x in range(w)]
        for y in range(h)
    ]
    
    return matrix


def game_loop(level_data, level_num):
    """Основний ігровий цикл"""
    global game_state
    
    # Розпаковка кортежу
    width, height, obstacles = level_data
    
    # Скидання стану
    game_state['score'] = 0
    game_state['speed'] = 0.2
    game_state['level'] = level_num
    game_state['visited_cells'] = set()
    
    # Створення матриці поля
    field = create_field_matrix(width, height, obstacles)
    
    # Початкова змійка (кортежі для координат)
    snake = [(7, 5), (6, 5), (5, 5)]
    direction = 'RIGHT'
    
    # Генерація їжі
    food = spawn_food_on_matrix(field, snake)
    food_type = 'normal'
    
    # Якщо випадково - бонусна їжа
    if random.random() < 0.2:
        food_type = 'bonus'
    
    running = True
    
    while running:
        draw_matrix(field, snake, food, food_type)
        
        # Показуємо меню
        print("S - Зберегти гру | Q - Вихід")
        
        new_dir = input_key(direction)
        
        if new_dir == 'QUIT':
            break
        elif new_dir == 'SAVE':
            save_game(snake, direction, food, food_type, field)
            print("Гру збережено!")
            time.sleep(1)
            continue
        
        direction = new_dir
        
        # Нова позиція
        new_head = get_new_position(snake[0], direction)
        
        # Перевірки
        if hit_obstacle(new_head, field) or new_head in snake:
            print("\n💥 Game Over!")
            show_stats()
            save_highscore()
            break
        
        # Додаємо в множину відвіданих клітинок
        game_state['visited_cells'].add(new_head)
        
        # Додаємо голову
        snake = [new_head] + list(snake)  # Конвертація в список
        
        # Перевірка їжі
        if new_head == food:
            points = config['food_types'][food_type]['points']
            game_state['score'] += points
            
            if game_state['score'] > game_state['high_score']:
                game_state['high_score'] = game_state['score']
            
            food = spawn_food_on_matrix(field, snake)
            food_type = 'bonus' if random.random() < 0.2 else 'normal'
            
            make_faster()
        else:
            # Використання зрізу для видалення хвоста
            snake = snake[:-1]
        
        time.sleep(game_state['speed'])


def create_field_matrix(w, h, obstacles):
    """
    Створює матрицю поля з перешкодами.
    Демонструє: матриці, list comprehension
    """
    # Копіюємо перешкоди якщо є
    if obstacles:
        # Використання list comprehension для копіювання
        field = [row[:] for row in obstacles]
    else:
        field = create_empty_matrix(w, h)
    
    return field


def draw_matrix(field, snake, food, food_type='normal'):
    """
    Малює поле використовуючи матрицю.
    Демонструє: робота з матрицями, enumerate
    """
    os.system('cls')
    
    print(f"Рахунок: {game_state['score']} | Рекорд: {game_state['high_score']} | Рівень: {game_state['level']}")
    print(f"Відвідано клітинок: {len(game_state['visited_cells'])}")
    print("=" * (len(field[0]) + 2))
    
    # Створюємо копію поля для відображення
    display = [row[:] for row in field]
    
    # Розміщуємо їжу
    fx, fy = food
    display[fy][fx] = config['food_types'][food_type]['symbol']
    
    # Розміщуємо змійку
    for i, (x, y) in enumerate(snake):
        if i == 0:
            display[y][x] = config['symbols']['head']
        else:
            display[y][x] = config['symbols']['body']
    
    # Малюємо (enumerate для індексів)
    for idx, row in enumerate(display):
        print(''.join(row))
    
    print("=" * (len(field[0]) + 2))


def spawn_food_on_matrix(field, snake):
    """
    Генерує їжу на матриці.
    Демонструє: list comprehension, множини
    """
    h, w = len(field), len(field[0])
    
    # List comprehension для знаходження вільних клітинок
    empty_cells = [
        (x, y) 
        for y in range(1, h-1) 
        for x in range(1, w-1)
        if field[y][x] == config['symbols']['empty'] and (x, y) not in snake
    ]
    
    if empty_cells:
        return random.choice(empty_cells)
    else:
        return (1, 1)


def hit_obstacle(pos, field):
    """Перевірка зіткнення з перешкодою"""
    x, y = pos
    
    if y < 0 or y >= len(field) or x < 0 or x >= len(field[0]):
        return True
    
    return field[y][x] == config['symbols']['wall']


def input_key(current):
    """Читає клавіші"""
    
    def opposite(d1, d2):
        opposites = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        return opposites.get(d1) == d2
    
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
            
            new = direction_map.get(key)
            if new and not opposite(current, new):
                return new
        
        elif key.lower() == b'q':
            return 'QUIT'
        elif key.lower() == b's':
            return 'SAVE'
    
    return current


def get_new_position(pos, direction):
    """Обчислює нову позицію"""
    x, y = pos
    
    moves = {
        'UP': lambda: (x, y - 1),
        'DOWN': lambda: (x, y + 1),
        'LEFT': lambda: (x - 1, y),
        'RIGHT': lambda: (x + 1, y)
    }
    
    return moves[direction]()


def make_faster():
    """Прискорює гру"""
    game_state['speed'] = max(0.05, game_state['speed'] - 0.02)


def show_stats():
    """
    Показує статистику.
    Демонструє: словники, множини
    """
    print(f"\nТвій рахунок: {game_state['score']}")
    print(f"Рекорд: {game_state['high_score']}")
    print(f"Відвідано унікальних клітинок: {len(game_state['visited_cells'])}")


def show_highscores():
    """
    Показує таблицю рекордів.
    Демонструє: читання файлу, зрізи, кортежі
    """
    print("\n" + "=" * 40)
    print("         ТОП-5 РЕКОРДІВ")
    print("=" * 40)
    
    try:
        with open('highscores.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Парсинг та сортування
        scores = []
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 3:
                score, name, date = parts
                scores.append((int(score), name, date))
        
        # Сортування за балами
        scores.sort(reverse=True)
        
        # Зріз - тільки топ-5
        top_scores = scores[:5]
        
        for i, (score, name, date) in enumerate(top_scores, 1):
            print(f"{i}. {name}: {score} балів ({date})")
        
    except FileNotFoundError:
        print("Рекордів поки немає")


def save_highscore():
    """
    Зберігає рекорд у файл.
    Демонструє: запис у текстовий файл, зіркові параметри
    """
    if game_state['score'] == 0:
        return
    
    name = input("\nВведи своє ім'я: ").strip() or "Гравець"
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Функція зі зірковими параметрами
    save_score_to_file(game_state['score'], name, date)


def save_score_to_file(*args, **kwargs):
    """
    Зберігає рекорд.
    Демонструє: *args та **kwargs
    """
    if args:
        score, name, date = args
    else:
        score = kwargs.get('score', 0)
        name = kwargs.get('name', 'Гравець')
        date = kwargs.get('date', datetime.now().strftime("%Y-%m-%d"))
    
    try:
        with open('highscores.txt', 'a', encoding='utf-8') as f:
            f.write(f"{score}|{name}|{date}\n")
        print("Рекорд збережено!")
    except Exception as e:
        print(f"Помилка збереження: {e}")


def save_game(snake, direction, food, food_type, field):
    """
    Зберігає гру в двійковий файл.
    Демонструє: pickle, двійкові файли
    """
    save_data = {
        'snake': snake,
        'direction': direction,
        'food': food,
        'food_type': food_type,
        'field': field,
        'game_state': game_state.copy()
    }
    
    # Збереження в бінарний файл
    with open('save.dat', 'wb') as f:
        pickle.dump(save_data, f)
    
    # Також в текстовий для ілюстрації
    with open('save.txt', 'w', encoding='utf-8') as f:
        f.write(f"Score: {game_state['score']}\n")
        f.write(f"Level: {game_state['level']}\n")
        f.write(f"Direction: {direction}\n")


def load_game():
    """
    Завантажує гру з файлу.
    Демонструє: pickle, читання двійкових файлів
    """
    try:
        with open('save.dat', 'rb') as f:
            save_data = pickle.load(f)
        
        print("Гру завантажено!")
        time.sleep(1)
        
        # Відновлюємо стан
        global game_state
        game_state = save_data['game_state']
        
        # Продовжуємо гру
        continue_loaded_game(save_data)
        
    except FileNotFoundError:
        print("Збережена гра не знайдена!")
        time.sleep(1)
        main()


def continue_loaded_game(save_data):
    """Продовжує завантажену гру"""
    snake = save_data['snake']
    direction = save_data['direction']
    food = save_data['food']
    food_type = save_data['food_type']
    field = save_data['field']
    
    running = True
    
    while running:
        draw_matrix(field, snake, food, food_type)
        print("S - Зберегти | Q - Вихід")
        
        new_dir = input_key(direction)
        
        if new_dir == 'QUIT':
            break
        elif new_dir == 'SAVE':
            save_game(snake, direction, food, food_type, field)
            print("Гру збережено!")
            time.sleep(1)
            continue
        
        direction = new_dir
        new_head = get_new_position(snake[0], direction)
        
        if hit_obstacle(new_head, field) or new_head in snake:
            print("\n💥 Game Over!")
            show_stats()
            save_highscore()
            break
        
        game_state['visited_cells'].add(new_head)
        snake = [new_head] + list(snake)
        
        if new_head == food:
            points = config['food_types'][food_type]['points']
            game_state['score'] += points
            
            if game_state['score'] > game_state['high_score']:
                game_state['high_score'] = game_state['score']
            
            food = spawn_food_on_matrix(field, snake)
            food_type = 'bonus' if random.random() < 0.2 else 'normal'
            make_faster()
        else:
            snake = snake[:-1]
        
        time.sleep(game_state['speed'])


# Додаткові функції для демонстрації критеріїв

def demo_slices(items):
    """
    Демонстрація зрізів.
    Демонструє: всі види зрізів
    """
    first_three = items[:3]      # Перші 3
    last_three = items[-3:]      # Останні 3
    middle = items[2:5]          # З 2 по 5
    every_second = items[::2]    # Кожен другий
    reversed_items = items[::-1] # Реверс
    
    return first_three, last_three, middle


def demo_tuple_unpacking():
    """Демонстрація розпакування кортежів"""
    coordinates = (10, 20)
    x, y = coordinates  # Розпакування
    
    # Множинне повернення (як кортеж)
    return x, y, x + y


def demo_set_operations():
    """
    Демонстрація операцій з множинами.
    Демонструє: множини та операції
    """
    visited = {(1, 2), (3, 4), (5, 6)}
    new_cells = {(5, 6), (7, 8), (9, 10)}
    
    # Об'єднання
    all_cells = visited | new_cells
    
    # Перетин
    common = visited & new_cells
    
    # Різниця
    unique = visited - new_cells
    
    return all_cells, common, unique


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nВихід!")
