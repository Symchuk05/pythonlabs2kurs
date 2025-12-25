# 📖 Пояснення Lab 4 - Де що знаходиться

## 🎯 Загальна структура

```
snake_game/              # Головний пакет
├── exceptions.py        # Винятки
├── __init__.py         # Публічний API
├── core/               # Ядро гри
│   ├── __init__.py
│   ├── position.py     # Клас Position
│   ├── food.py         # Їжа (спадкування)
│   ├── snake.py        # Змійка (послідовності)
│   └── game_field.py   # Поле
├── game/               # Ігровий движок
│   ├── __init__.py
│   ├── state.py        # Стан гри
│   └── engine.py       # Головний движок
└── utils/              # Утиліти
    ├── __init__.py
    ├── decorators.py   # Декоратори + замикання
    └── generators.py   # Генератори
```

---

## 1️⃣ ВИНЯТКИ (exceptions.py)

### Де знаходиться
📁 `snake_game/exceptions.py` → [**GitHub**](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py)

### Що реалізовано
- **GameError** - базовий клас для всіх ігрових помилок → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L1-L8)
- **CollisionError** - зіткнення змійки → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L11-L18)
- **InvalidMoveError** - невірний рух → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L21-L28)
- **LevelLoadError** - помилка завантаження рівня → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L31-L38)
- **SaveGameError** - помилка збереження → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L41-L48)
- **InvalidPositionError** - невірна позиція → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py#L51-L58)

### Як працює
```python
# Створення власного винятку
raise CollisionError("Змійка вдарилась об стіну", position=(5, 10))

# Ловлення винятку
try:
    self._game_loop()
except CollisionError as e:
    print(f"Game Over! {e}")
```

### Де використовується
- `engine.py` - [рядок 192](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L192), [рядок 195](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L195) (викидання)
- `engine.py` - [рядок 124](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L124), [рядок 180](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L180), [рядок 295](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L295) (ловлення)

---

## 2️⃣ МОДУЛІ

### Структура модулів
- `position.py` - робота з координатами
- `food.py` - типи їжі
- `snake.py` - логіка змійки
- `game_field.py` - ігрове поле
- `state.py` - стан гри
- `engine.py` - головний движок
- `decorators.py` - декоратори
- `generators.py` - генератори

### Імпорти між модулями
```python
# В engine.py
from ..core import Position, Snake, Food
from ..exceptions import CollisionError
from ..utils.generators import level_parser
```

---

## 3️⃣ ПАКЕТИ

### Головний пакет: snake_game/

**__init__.py** експортує публічний API:
```python
from .core import Position, Snake, Food
from .game import SnakeGame
from .exceptions import GameError, CollisionError
```

### Підпакет: core/

Містить основні класи гри.

**Як працює:**
```python
# Можна імпортувати так:
from snake_game.core import Snake, Position

# Або через головний пакет:
from snake_game import Snake
```

### Підпакет: game/

Містить ігровий движок та стан.

### Підпакет: utils/

Містить допоміжні утиліти.

---

## 4️⃣ АНОТАЦІЇ ТИПІВ

### Де дивитись
Всі файли мають повні анотації типів!

### Приклади

**position.py:**
```python
def __init__(self, x: int, y: int) -> None:
    self.__x: int = x
    
def move(self, direction: str) -> 'Position':
    moves: Dict[str, Tuple[int, int]] = {...}
```

**snake.py:**
```python
def __init__(self, initial_positions: List[Union[Position, Tuple[int, int]]]) -> None:
    self.__body: List[Position] = []
    
def __getitem__(self, index: int) -> Position:
    return self.__body[index]
```

**engine.py:**
```python
def _new_game(self, level_data: Optional[Tuple] = None, level_num: int = 1) -> None:
    ...
```

### Складні типи
```python
from typing import List, Tuple, Optional, Dict, Set, Union, Iterator, Generator
```

---

## 5️⃣ ГЕНЕРАТОРИ (generators.py)

### Де знаходиться
📁 `snake_game/utils/generators.py` → [**GitHub**](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py)

### 1. level_parser → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L5-L35)
**Що робить:** Читає файл рівнів та повертає їх по одному

```python
def level_parser(filename: str) -> Generator[Tuple[int, int, List[List[str]]], None, None]:
    for block in blocks:
        # Парсинг рівня
        yield (width, height, matrix)
```

**Де використовується:** [`engine.py`, рядок 335](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L335)

**Використання:**
```python
for width, height, matrix in level_parser('levels.txt'):
    levels.append((width, height, matrix))
```

### 2. highscore_reader → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L38-L52)
**Що робить:** Читає рекорди з файлу по одному

**Де використовується:** [`engine.py`, рядок 405](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L405)

### 3. spiral_positions → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L55-L80)
**Що робить:** Генерує позиції по спіралі від центру

**Переваги генераторів:**
- ✅ Економія пам'яті (lazy evaluation)
- ✅ Не завантажують весь файл в пам'ять
- ✅ Можна зупинити в будь-який момент

---

## 6️⃣ ДЕКОРАТОРИ + ЗАМИКАННЯ (decorators.py)

### Де знаходиться
📁 `snake_game/utils/decorators.py` → [**GitHub**](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py)

### 1. @timer → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L5-L18)
**Що робить:** Вимірює час виконання функції

```python
@timer
def _game_loop(self) -> None:
    ...
# Виведе: ⏱️ '_game_loop' виконувався 45.23 сек
```

**Де використовується:** [`engine.py`, рядок 147](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L147)

### 2. @cache_result → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L21-L35)
**Що робить:** Кешує результати функції

**Демонструє замикання:**
```python
def cache_result(func):
    cache: dict = {}  # Ця змінна "захоплена" wrapper
    
    def wrapper(*args, **kwargs):
        if key not in cache:
            cache[key] = func(*args, **kwargs)  # Доступ до cache
        return cache[key]
    return wrapper
```

### 3. @retry → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L38-L56)
**Параметризований декоратор (подвійне замикання):**
```python
def retry(max_attempts: int = 3):  # Зовнішня функція
    def decorator(func):            # Декоратор
        def wrapper(*args):         # Wrapper
            attempts = 0            # Захоплена змінна
            ...
```

### 4. create_score_tracker() → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L59-L82)
**Фабрика функцій з замиканням:**

```python
def create_score_tracker():
    scores: list = []  # Захоплена всіма функціями
    
    def add_score(score: int):
        scores.append(score)  # Використання scores
    
    def get_average():
        return sum(scores) / len(scores)  # Використання scores
    
    return add_score, get_average
```

**Як працює:**
```python
add, avg = create_score_tracker()
add(100)
add(200)
print(avg())  # 150.0
```

**Демонструє:**
- Лексичне замикання (функції "пам'ятають" scores)
- Ізоляція стану (кожен трекер має свій scores)

---

## 7️⃣ ПОСЛІДОВНОСТІ (snake.py)

### Де знаходиться
📁 `snake_game/core/snake.py` → [**GitHub**](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py)

### Реалізовані методи

**1. `__len__`** - довжина змійки → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L26-L27)
```python
def __len__(self) -> int:
    return len(self.__body)

# Використання
print(len(snake))  # 5
```

**2. `__getitem__`** - доступ за індексом → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L29-L30)
```python
def __getitem__(self, index: int) -> Position:
    return self.__body[index]

# Використання
head = snake[0]
tail = snake[-1]
```

**3. `__contains__`** - перевірка наявності → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L32-L33)
```python
def __contains__(self, position) -> bool:
    return position in self.__body

# Використання
if pos in snake:
    print("Зіткнення!")
```

**4. `__iter__`** - ітерація → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L35-L36)
```python
def __iter__(self) -> Iterator[Position]:
    return iter(self.__body)

# Використання
for segment in snake:
    print(segment)
```

**5. `__reversed__`** - зворотна ітерація → [код](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L38-L39)
```python
def __reversed__(self) -> Iterator[Position]:
    return reversed(self.__body)

# Використання
for segment in reversed(snake):
    print(segment)
```

**Де використовується:** [`game_field.py`, рядок 71](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L71)

---

## 8️⃣ ТЕСТУВАННЯ

### Де знаходиться
📁 `tests/` → [**GitHub**](https://github.com/Symchuk05/pythonlabs2kurs/tree/main/tests)

### Структура тестів
- [`test_position.py`](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_position.py) - 15 тестів для Position
- [`test_snake.py`](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_snake.py) - 16 тестів для Snake
- [`test_food.py`](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_food.py) - 12 тестів для Food
- [`test_decorators.py`](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_decorators.py) - 5 тестів для декораторів
- [`test_exceptions.py`](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_exceptions.py) - 9 тестів для винятків

### Приклад тесту

```python
class TestSnake(unittest.TestCase):
    def test_getitem(self):
        """Тест доступу за індексом"""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertEqual(snake[0], Position(5, 5))  # Голова
        self.assertEqual(snake[-1], Position(3, 5))  # Хвіст
```
→ [Дивитись тест](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/tests/test_snake.py#L34-L39)

### Запуск тестів
```bash
python -m unittest discover -s tests -v
```

**Результат:** 57/57 тестів пройшли ✅

---

## 🎓 ДЛЯ ЗАХИСТУ ЛАБИ

### Питання 1: "Де у вас винятки?"
**Відповідь:** `snake_game/exceptions.py` - 6 класів винятків з ієрархією. Використовуються в `engine.py` для обробки помилок гри.

### Питання 2: "Покажіть анотації типів"
**Відповідь:** Всі файли мають анотації. Приклад у `snake.py`:
```python
def __init__(self, initial_positions: List[Union[Position, Tuple[int, int]]]) -> None
```

### Питання 3: "Де генератори?"
**Відповідь:** `utils/generators.py` - 6 генераторів. `level_parser` використовується в `engine.py` для завантаження рівнів.

### Питання 4: "Покажіть замикання"
**Відповідь:** `decorators.py` - `create_score_tracker()` демонструє замикання. Змінна `scores` захоплюється всіма внутрішніми функціями.

### Питання 5: "Де декоратори?"
**Відповідь:** `decorators.py` - 6 декораторів. `@timer` використовується  в `engine.py` на методі `_game_loop`.

### Питання 6: "Покажіть послідовності"
**Відповідь:** `snake.py` - клас Snake реалізує 5 методів протоколу послідовності: `__len__`, `__getitem__`, `__iter__`, `__contains__`, `__reversed__`.

### Питання 7: "Скільки тестів?"
**Відповідь:** 57 тестів у 5 файлах. Всі пройшли успішно.

---

## 📋 ШВИДКА НАВІГАЦІЯ

| Вимога | Файл | GitHub Link |
|--------|------|-------------|
| Винятки | `exceptions.py` | [Всі класи](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py) |
| Генератори | `generators.py` | [level_parser](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L5-L35), [highscore_reader](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L38-L52) |
| Декоратори | `decorators.py` | [timer](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L5-L18), [cache_result](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L21-L35), [retry](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L38-L56) |
| Замикання | `decorators.py` | [create_score_tracker](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L59-L82) |
| Послідовності | `snake.py` | [__len__](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L26-L27), [__getitem__](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L29-L30), [__iter__](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L35-L36) |
| Анотації | Всі файли | [Position](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/position.py), [Snake](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py) |
| Пакети | `__init__.py` | [Головний](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/__init__.py), [Core](https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/__init__.py) |
| Тести | `tests/` | [57 тестів](https://github.com/Symchuk05/pythonlabs2kurs/tree/main/tests) |

---

**Підготував:** Студент ХНУРЕ  
**Дата:** 25.12.2024  
**Lab:** 4  
**Бали:** 79/79 ⭐⭐⭐⭐⭐
