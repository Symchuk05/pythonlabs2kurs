"""
Тести для винятків.

Демонструє: Тестування власних винятків
Вимоги Lab 4: Тестування
"""

import unittest
from snake_game.exceptions import (
    GameError,
    CollisionError,
    InvalidMoveError,
    LevelLoadError,
    SaveGameError,
    InvalidPositionError
)


class TestExceptions(unittest.TestCase):
    """Тести для винятків."""
    
    def test_game_error_basic(self) -> None:
        """Тест базового винятку GameError."""
        error = GameError("Тестова помилка")
        self.assertEqual(str(error), "Тестова помилка")
    
    def test_game_error_with_details(self) -> None:
        """Тест GameError з деталями."""
        error = GameError("Помилка", "Додаткова інфо")
        error_str = str(error)
        self.assertIn("Помилка", error_str)
        self.assertIn("Додаткова інфо", error_str)
    
    def test_collision_error_inheritance(self) -> None:
        """Тест що CollisionError успадковує GameError."""
        error = CollisionError()
        self.assertIsInstance(error, GameError)
        self.assertIsInstance(error, CollisionError)
    
    def test_collision_error_with_position(self) -> None:
        """Тест CollisionError з позицією."""
        error = CollisionError("Зіткнення", position=(5, 10))
        self.assertEqual(error.position, (5, 10))
        self.assertIn("5, 10", str(error))
    
    def test_invalid_move_error(self) -> None:
        """Тест InvalidMoveError."""
        error = InvalidMoveError("Невірний рух", direction="INVALID")
        self.assertIsInstance(error, GameError)
        self.assertEqual(error.direction, "INVALID")
    
    def test_level_load_error(self) -> None:
        """Тест LevelLoadError."""
        error = LevelLoadError("Не вдалось завантажити", filename="levels.txt")
        self.assertIsInstance(error, GameError)
        self.assertEqual(error.filename, "levels.txt")
        self.assertIn("levels.txt", str(error))
    
    def test_save_game_error(self) -> None:
        """Тест SaveGameError."""
        error = SaveGameError("Не вдалось зберегти", filename="save.dat")
        self.assertIsInstance(error, GameError)
        self.assertEqual(error.filename, "save.dat")
    
    def test_invalid_position_error(self) -> None:
        """Тест InvalidPositionError."""
        error = InvalidPositionError("Позиція за межами", position=(-1, 5))
        self.assertIsInstance(error, GameError)
        self.assertEqual(error.position, (-1, 5))
    
    def test_exception_raising(self) -> None:
        """Тест викидання та ловлення винятків."""
        with self.assertRaises(GameError):
            raise GameError("Тест")
        
        with self.assertRaises(CollisionError):
            raise CollisionError("Зіткнення")
    
    def test_catching_base_exception(self) -> None:
        """Тест ловлення через базовий клас."""
        try:
            raise CollisionError("Тест")
        except GameError as e:
            # Має спіймати як GameError
            self.assertIsInstance(e, CollisionError)
            self.assertIsInstance(e, GameError)


if __name__ == '__main__':
    unittest.main()
