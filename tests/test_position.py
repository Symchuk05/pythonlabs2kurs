"""
Тести для класу Position.

Демонструє: Юніт-тестування, assertions, type hints
Вимоги Lab 4: Тестування
"""

import unittest
from snake_game.core.position import Position


class TestPosition(unittest.TestCase):
    """Тести для класу Position."""
    
    def test_creation(self) -> None:
        """Тест створення позиції."""
        pos = Position(5, 10)
        self.assertEqual(pos.x, 5)
        self.assertEqual(pos.y, 10)
    
    def test_equality_with_position(self) -> None:
        """Тест порівняння з іншою позицією."""
        pos1 = Position(5, 5)
        pos2 = Position(5, 5)
        pos3 = Position(5, 6)
        
        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)
    
    def test_equality_with_tuple(self) -> None:
        """Тест порівняння з кортежем."""
        pos = Position(5, 10)
        self.assertEqual(pos, (5, 10))
        self.assertNotEqual(pos, (5, 11))
    
    def test_hash(self) -> None:
        """Тест хешування для використання в множинах."""
        pos1 = Position(5, 5)
        pos2 = Position(5, 5)
        pos3 = Position(6, 6)
        
        # Однакові позиції мають однаковий хеш
        self.assertEqual(hash(pos1), hash(pos2))
        
        # Можна використовувати в множинах
        positions = {pos1, pos2, pos3}
        self.assertEqual(len(positions), 2)  # pos1 і pos2 - однакові
    
    def test_str(self) -> None:
        """Тест строкового представлення."""
        pos = Position(5, 10)
        self.assertEqual(str(pos), "(5, 10)")
    
    def test_repr(self) -> None:
        """Тест формального представлення."""
        pos = Position(5, 10)
        self.assertEqual(repr(pos), "Position(5, 10)")
    
    def test_to_tuple(self) -> None:
        """Тест конвертації в кортеж."""
        pos = Position(7, 8)
        tup = pos.to_tuple()
        self.assertEqual(tup, (7, 8))
        self.assertIsInstance(tup, tuple)
    
    def test_move_up(self) -> None:
        """Тест руху вгору."""
        pos = Position(5, 5)
        new_pos = pos.move('UP')
        self.assertEqual(new_pos, (5, 4))
    
    def test_move_down(self) -> None:
        """Тест руху вниз."""
        pos = Position(5, 5)
        new_pos = pos.move('DOWN')
        self.assertEqual(new_pos, (5, 6))
    
    def test_move_left(self) -> None:
        """Тест руху вліво."""
        pos = Position(5, 5)
        new_pos = pos.move('LEFT')
        self.assertEqual(new_pos, (4, 5))
    
    def test_move_right(self) -> None:
        """Тест руху вправо."""
        pos = Position(5, 5)
        new_pos = pos.move('RIGHT')
        self.assertEqual(new_pos, (6, 5))
    
    def test_move_invalid(self) -> None:
        """Тест невалідного напрямку (має повернути ту ж позицію)."""
        pos = Position(5, 5)
        new_pos = pos.move('INVALID')
        self.assertEqual(new_pos, (5, 5))
    
    def test_immutability(self) -> None:
        """Тест незмінності координат."""
        pos = Position(5, 5)
        # Координати тільки для читання
        with self.assertRaises(AttributeError):
            pos.x = 10  # type: ignore


if __name__ == '__main__':
    unittest.main()
