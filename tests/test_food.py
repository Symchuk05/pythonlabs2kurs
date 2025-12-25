"""
Тести для класів їжі.

Демонструє: Тестування спадкування
Вимоги Lab 4: Тестування
"""

import unittest
from snake_game.core.food import Food, NormalFood, BonusFood
from snake_game.core.position import Position


class TestFood(unittest.TestCase):
    """Тести для базового класу Food."""
    
    def test_creation_with_tuple(self) -> None:
        """Тест створення їжі з кортежу."""
        food = Food((10, 10))
        self.assertEqual(food.position, Position(10, 10))
    
    def test_creation_with_position(self) -> None:
        """Тест створення їжі з Position."""
        pos = Position(5, 5)
        food = Food(pos)
        self.assertEqual(food.position, pos)
    
    def test_default_points(self) -> None:
        """Тест початкових балів."""
        food = Food((5, 5))
        self.assertEqual(food.points, 10)
    
    def test_default_symbol(self) -> None:
        """Тест початкового символу."""
        food = Food((5, 5))
        self.assertEqual(food.symbol, '*')
    
    def test_str(self) -> None:
        """Тест строкового представлення."""
        food = Food((5, 5))
        result = str(food)
        self.assertIn("Food", result)
        self.assertIn("10", result)


class TestNormalFood(unittest.TestCase):
    """Тести для NormalFood."""
    
    def test_inheritance(self) -> None:
        """Тест що NormalFood успадковує Food."""
        food = NormalFood((5, 5))
        self.assertIsInstance(food, Food)
        self.assertIsInstance(food, NormalFood)
    
    def test_points(self) -> None:
        """Тест балів для звичайної їжі."""
        food = NormalFood((5, 5))
        self.assertEqual(food.points, 10)
    
    def test_symbol(self) -> None:
        """Тест символу для звичайної їжі."""
        food = NormalFood((5, 5))
        self.assertEqual(food.symbol, '*')
    
    def test_str(self) -> None:
        """Тест строкового представлення."""
        food = NormalFood((5, 5))
        result = str(food)
        self.assertIn("NormalFood", result)
        self.assertIn("10", result)


class TestBonusFood(unittest.TestCase):
    """Тести для BonusFood."""
    
    def test_inheritance(self) -> None:
        """Тест що BonusFood успадковує Food."""
        food = BonusFood((5, 5))
        self.assertIsInstance(food, Food)
        self.assertIsInstance(food, BonusFood)
    
    def test_points(self) -> None:
        """Тест балів для бонусної їжі."""
        food = BonusFood((5, 5))
        self.assertEqual(food.points, 25)
    
    def test_symbol(self) -> None:
        """Тест символу для бонусної їжі."""
        food = BonusFood((5, 5))
        self.assertEqual(food.symbol, '$')
    
    def test_str(self) -> None:
        """Тест строкового представлення."""
        food = BonusFood((5, 5))
        result = str(food)
        self.assertIn("BonusFood", result)
        self.assertIn("25", result)
    
    def test_more_points_than_normal(self) -> None:
        """Тест що бонусна їжа дає більше балів."""
        normal = NormalFood((5, 5))
        bonus = BonusFood((6, 6))
        self.assertGreater(bonus.points, normal.points)


if __name__ == '__main__':
    unittest.main()
