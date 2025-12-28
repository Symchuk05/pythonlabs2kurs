# Головний ігровий движок

import msvcrt
import os
import sys
import time
import random
import pickle
from datetime import datetime
from typing import List, Tuple, Optional

# Налаштування UTF-8 для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.system('chcp 65001 >nul 2>&1')

from ..core import Position, Snake, Food, NormalFood, BonusFood, GameField
from ..exceptions import CollisionError, SaveGameError, LevelLoadError
from ..utils.generators import level_parser, highscore_reader
from ..utils.decorators import timer
from .state import GameState


class SnakeGame:
    """Головний клас ігрового движка"""
    
    def __init__(self) -> None:
        self._state: GameState = GameState()
        self._field: Optional[GameField] = None
        self._snake: Optional[Snake] = None
        self._food: Optional[Food] = None
        self._levels: List[Tuple[int, int, List[List[str]]]] = []
        
        try:
            self._levels = self._load_levels()
            print(f"✓ Завантажено рівнів: {len(self._levels)}")
        except LevelLoadError as e:
            print(f"⚠️  {e}")
            self._levels = self._create_default_levels()
    
    def start(self) -> None:
        """Запуск гри з головним меню"""
        print("=" * 40)
        print("         ГРА ЗМІЙКА 4.0 (Package)")
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
    
    def _select_level(self) -> None:
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
    
    def _new_game(self, level_data: Optional[Tuple] = None, level_num: int = 1) -> None:
        """Початок нової гри"""
        if level_data is None:
            width, height, obstacles = 15, 10, None
        else:
            width, height, obstacles = level_data
        
        self._field = GameField(width, height, obstacles)
        self._snake = Snake([
            (width // 2, height // 2),
            (width // 2 - 1, height // 2),
            (width // 2 - 2, height // 2)
        ])
        self._state.reset(level_num)
        
        self._spawn_food()
        
        try:
            self._game_loop()
        except CollisionError as e:
            print(f"\n💥 Game Over! {e}")
            print(f"Твій рахунок: {self._state.score}")
            print(f"Рекорд: {self._state.high_score}")
            if self._snake:
                print(f"Відвідано клітинок: {self._snake.get_visited_count()}")
            self._save_highscore()
    
    def _spawn_food(self) -> None:
        """Генерація їжі"""
        if not self._field or not self._snake:
            return
        
        free_cells = self._field.get_free_cells(self._snake)
        
        if free_cells:
            pos = random.choice(free_cells)
            if random.random() < 0.2:
                self._food = BonusFood(pos)
            else:
                self._food = NormalFood(pos)
    
    @timer
    def _game_loop(self) -> None:
        """Основний ігровий цикл"""
        if not self._field or not self._snake or not self._food:
            return
        
        running = True
        
        while running:
            self._field.draw(self._snake, self._food)
            print(self._state)
            print(f"Довжина змійки: {len(self._snake)}")
            print(f"Відвідано клітинок: {self._snake.get_visited_count()}")
            print(f"Поточна їжа: {self._food}")
            print("\nS - Зберегти | Q - Вихід")
            
            new_dir = self._input_key()
            
            if new_dir == 'QUIT':
                break
            elif new_dir == 'SAVE':
                try:
                    self._save_game()
                    print("✓ Гру збережено!")
                    time.sleep(1)
                    continue
                except SaveGameError as e:
                    print(f"❌ Помилка збереження: {e}")
                    time.sleep(1)
                    continue
            elif new_dir:
                self._snake.direction = new_dir
            
            self._snake.move()
            
            if self._field.is_obstacle(self._snake.head):
                raise CollisionError("Змійка вдарилась об стіну", self._snake.head.to_tuple())
            
            if self._snake.check_collision():
                raise CollisionError("Змійка з'їла сама себе", self._snake.head.to_tuple())
            
            if self._snake.head == self._food.position:
                self._state = self._state + self._food.points
                self._state.make_faster()
                self._snake.move(grow=True)
                self._spawn_food()
            
            time.sleep(self._state.speed)
    
    def _input_key(self) -> Optional[str]:
        """Читання клавіатури"""
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
    
    def _save_game(self) -> None:
        """Збереження гри"""
        if not self._snake or not self._food:
            raise SaveGameError("Неможливо зберегти: гра не ініціалізована")
        
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
        
        try:
            with open('save_oop.dat', 'wb') as f:
                pickle.dump(save_data, f)
        except Exception as e:
            raise SaveGameError(f"Не вдалось записати: {e}", "save_oop.dat")
    
    def _load_game(self) -> None:
        """Завантаження збереженої гри"""
        try:
            with open('save_oop.dat', 'rb') as f:
                save_data = pickle.load(f)
            
            print("✓ Гру завантажено!")
            time.sleep(1)
            
            self._field = GameField(15, 10)
            self._snake = Snake(save_data['snake_body'])
            self._snake._direction = save_data['snake_direction']
            
            if save_data['food_type'] == 'BonusFood':
                self._food = BonusFood(save_data['food_pos'])
            else:
                self._food = NormalFood(save_data['food_pos'])
            
            self._state = GameState()
            self._state._GameState__score = save_data['state']['score']
            self._state._GameState__high_score = save_data['state']['high_score']
            self._state._speed = save_data['state']['speed']
            self._state._level = save_data['state']['level']
            
            try:
                self._game_loop()
            except CollisionError as e:
                print(f"\n💥 Game Over! {e}")
                print(f"Твій рахунок: {self._state.score}")
                self._save_highscore()
            
        except FileNotFoundError:
            print("❌ Збережена гра не знайдена!")
            time.sleep(1)
            self.start()
        except Exception as e:
            raise SaveGameError(f"Не вдалось завантажити: {e}", "save_oop.dat")
    
    def _save_highscore(self) -> None:
        """Збереження рекорду"""
        if self._state.score == 0:
            return
        
        name = input("\nВведи своє ім'я: ").strip() or "Гравець"
        date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open('highscores.txt', 'a', encoding='utf-8') as f:
                f.write(f"{self._state.score}|{name}|{date}\n")
            print("✓ Рекорд збережено!")
        except Exception as e:
            print(f"❌ Помилка збереження рекорду: {e}")
    
    def _load_levels(self) -> List[Tuple[int, int, List[List[str]]]]:
        """Завантаження рівнів через генератор"""
        levels = []
        
        for level_data in level_parser('levels.txt'):
            levels.append(level_data)
            print(f"  ✓ Рівень {len(levels)}: {level_data[0]}x{level_data[1]}")
        
        if not levels:
            raise LevelLoadError("Не знайдено жодного рівня", "levels.txt")
        
        return levels
    
    def _create_default_levels(self) -> List[Tuple[int, int, List[List[str]]]]:
        """Створення дефолтних рівнів"""
        levels = []
        
        levels.append((15, 10, None))
        
        matrix = self._create_level_with_obstacles(20, 15, [(10, 7), (10, 8)])
        levels.append((20, 15, matrix))
        
        matrix = self._create_level_with_obstacles(
            25, 15,
            [(12, 5), (12, 6), (12, 7), (12, 8), (12, 9)]
        )
        levels.append((25, 15, matrix))
        
        return levels
    
    def _create_level_with_obstacles(
        self,
        width: int,
        height: int,
        obstacle_positions: List[Tuple[int, int]]
    ) -> List[List[str]]:
        """Створення матриці рівня з перешкодами"""
        matrix = [
            ['#' if x == 0 or x == width-1 or y == 0 or y == height-1 
             else ' '
             for x in range(width)]
            for y in range(height)
        ]
        
        for x, y in obstacle_positions:
            if 0 < x < width-1 and 0 < y < height-1:
                matrix[y][x] = '#'
        
        return matrix
    
    def _show_highscores(self) -> None:
        """Показати таблицю рекордів"""
        print("\n" + "=" * 40)
        print("         ТОП-5 РЕКОРДІВ")
        print("=" * 40)
        
        try:
            scores = []
            for score, name, date in highscore_reader('highscores.txt', limit=100):
                scores.append((score, name, date))
            
            scores.sort(key=lambda x: x[0], reverse=True)
            top_scores = scores[:5]
            
            for i, (score, name, date) in enumerate(top_scores, 1):
                print(f"{i}. {name}: {score} балів ({date})")
            
        except FileNotFoundError:
            print("Рекордів поки немає")
