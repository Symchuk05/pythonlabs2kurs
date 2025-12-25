"""
Тести для декораторів.

Демонструє: Тестування декораторів, лексичних замикань
Вимоги Lab 4: Тестування
"""

import sys
from pathlib import Path

# Додаємо кореневу директорію проєкту до sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import unittest
import time
from snake_game.utils.decorators import (
    timer, cache_result, limit_calls, create_score_tracker
)


class TestDecorators(unittest.TestCase):
    """Тести для декораторів."""
    
    def test_timer_decorator(self) -> None:
        """Тест декоратора timer."""
        
        @timer
        def slow_function() -> int:
            time.sleep(0.1)
            return 42
        
        # Функція має працювати нормально
        result = slow_function()
        self.assertEqual(result, 42)
    
    def test_cache_result_decorator(self) -> None:
        """Тест декоратора кешування."""
        call_count = 0
        
        @cache_result
        def expensive_function(n: int) -> int:
            nonlocal call_count
            call_count += 1
            return n * 2
        
        # Перший виклик
        result1 = expensive_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count, 1)
        
        # Другий виклик з тими ж аргументами - має використати кеш
        result2 = expensive_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)  # Не збільшився!
        
        # Виклик з іншими аргументами
        result3 = expensive_function(10)
        self.assertEqual(result3, 20)
        self.assertEqual(call_count, 2)
    
    def test_limit_calls_decorator(self) -> None:
        """Тест декоратора обмеження викликів."""
        
        @limit_calls(3)
        def limited_function() -> str:
            return "OK"
        
        # Перші 3 виклики мають працювати
        self.assertEqual(limited_function(), "OK")
        self.assertEqual(limited_function(), "OK")
        self.assertEqual(limited_function(), "OK")
        
        # 4-й виклик має викинути виняток
        with self.assertRaises(RuntimeError):
            limited_function()
    
    def test_create_score_tracker(self) -> None:
        """Тест фабрики функцій з замиканням."""
        add_score, get_average, get_all = create_score_tracker()
        
        # Початково порожньо
        self.assertEqual(get_average(), 0.0)
        self.assertEqual(get_all(), [])
        
        # Додаємо бали
        add_score(100)
        add_score(200)
        add_score(300)
        
        # Перевіряємо середнє
        self.assertEqual(get_average(), 200.0)
        
        # Перевіряємо всі бали
        all_scores = get_all()
        self.assertEqual(all_scores, [100, 200, 300])
    
    def test_closure_isolation(self) -> None:
        """Тест ізоляції замикань."""
        # Створюємо два незалежні трекери
        add1, avg1, all1 = create_score_tracker()
        add2, avg2, all2 = create_score_tracker()
        
        # Додаємо різні бали
        add1(100)
        add1(200)
        
        add2(50)
        
        # Трекери мають бути ізольовані
        self.assertEqual(avg1(), 150.0)
        self.assertEqual(avg2(), 50.0)
        self.assertEqual(len(all1()), 2)
        self.assertEqual(len(all2()), 1)


if __name__ == '__main__':
    unittest.main()
