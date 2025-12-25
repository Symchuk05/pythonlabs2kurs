"""
Тести для класу Snake.

Демонструє: Тестування послідовностей, ітераторів
Вимоги Lab 4: Тестування
"""

import unittest
from snake_game.core.snake import Snake
from snake_game.core.position import Position


class TestSnake(unittest.TestCase):
    """Тести для класу Snake."""
    
    def test_creation(self) -> None:
        """Тест створення змійки."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertEqual(len(snake), 3)
    
    def test_head_property(self) -> None:
        """Тест отримання голови змійки."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertEqual(snake.head, Position(5, 5))
    
    def test_direction_default(self) -> None:
        """Тест початкового напрямку."""
        snake = Snake([(5, 5), (4, 5)])
        self.assertEqual(snake.direction, 'RIGHT')
    
    def test_direction_setter_valid(self) -> None:
        """Тест зміни напрямку."""
        snake = Snake([(5, 5), (4, 5)])
        snake.direction = 'UP'
        self.assertEqual(snake.direction, 'UP')
    
    def test_direction_setter_opposite(self) -> None:
        """Тест заборони руху в протилежний бік."""
        snake = Snake([(5, 5), (4, 5)])
        snake._direction = 'RIGHT'
        snake.direction = 'LEFT'  # Протилежний напрямок
        self.assertEqual(snake.direction, 'RIGHT')  # Має залишитись RIGHT
    
    def test_len(self) -> None:
        """Тест методу __len__."""
        snake = Snake([(5, 5), (4, 5), (3, 5), (2, 5)])
        self.assertEqual(len(snake), 4)
    
    def test_contains(self) -> None:
        """Тест методу __contains__."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertIn(Position(5, 5), snake)
        self.assertIn(Position(4, 5), snake)
        self.assertNotIn(Position(10, 10), snake)
    
    def test_getitem(self) -> None:
        """Тест доступу за індексом."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertEqual(snake[0], Position(5, 5))  # Голова
        self.assertEqual(snake[1], Position(4, 5))
        self.assertEqual(snake[-1], Position(3, 5))  # Хвіст
    
    def test_iter(self) -> None:
        """Тест ітерації по змійці."""
        positions = [(5, 5), (4, 5), (3, 5)]
        snake = Snake(positions)
        
        iterated = []
        for segment in snake:
            iterated.append(segment)
        
        self.assertEqual(len(iterated), 3)
        self.assertEqual(iterated[0], Position(5, 5))
    
    def test_reversed(self) -> None:
        """Тест зворотної ітерації."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        reversed_list = list(reversed(snake))
        
        self.assertEqual(reversed_list[0], Position(3, 5))
        self.assertEqual(reversed_list[-1], Position(5, 5))
    
    def test_move_without_grow(self) -> None:
        """Тест руху без зростання."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        initial_length = len(snake)
        
        snake.move(grow=False)
        
        self.assertEqual(len(snake), initial_length)  # Довжина не змінилась
        self.assertEqual(snake.head, Position(6, 5))  # Голова змістилась
    
    def test_move_with_grow(self) -> None:
        """Тест руху зі зростанням."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        initial_length = len(snake)
        
        snake.move(grow=True)
        
        self.assertEqual(len(snake), initial_length + 1)  # Довжина збільшилась
        self.assertEqual(snake.head, Position(6, 5))
    
    def test_check_collision_false(self) -> None:
        """Тест відсутності зіткнення."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        self.assertFalse(snake.check_collision())
    
    def test_check_collision_true(self) -> None:
        """Тест зіткнення з собою."""
        # Створюємо змійку що вдарилась сама в себе
        snake = Snake([(5, 5), (4, 5), (3, 5), (5, 5)])
        self.assertTrue(snake.check_collision())
    
    def test_visited_cells(self) -> None:
        """Тест підрахунку відвіданих клітинок."""
        snake = Snake([(5, 5), (4, 5), (3, 5)])
        initial_count = snake.get_visited_count()
        
        snake.move()
        snake.move()
        
        # Кількість відвіданих клітинок має збільшитись
        self.assertGreater(snake.get_visited_count(), initial_count)


if __name__ == '__main__':
    unittest.main()
