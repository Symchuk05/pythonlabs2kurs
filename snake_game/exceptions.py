# Власні винятки для гри

from typing import Optional


class GameError(Exception):
    """Базовий виняток для всіх ігрових помилок"""
    
    def __init__(self, message: str, details: Optional[str] = None) -> None:
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} (Деталі: {self.details})"
        return self.message


class CollisionError(GameError):
    """Зіткнення змійки з перешкодою"""
    
    def __init__(self, message: str = "Зіткнення", position: Optional[tuple] = None) -> None:
        details = f"Позиція: {position}" if position else None
        super().__init__(message, details)
        self.position = position


class InvalidMoveError(GameError):
    """Невірний рух"""
    
    def __init__(self, message: str = "Невірний рух", direction: Optional[str] = None) -> None:
        details = f"Напрямок: {direction}" if direction else None
        super().__init__(message, details)
        self.direction = direction


class LevelLoadError(GameError):
    """Помилка завантаження рівня"""
    
    def __init__(self, message: str = "Не вдалось завантажити рівень", filename: Optional[str] = None) -> None:
        details = f"Файл: {filename}" if filename else None
        super().__init__(message, details)
        self.filename = filename


class SaveGameError(GameError):
    """Помилка збереження/завантаження гри"""
    
    def __init__(self, message: str = "Помилка збереження", filename: Optional[str] = None) -> None:
        details = f"Файл: {filename}" if filename else None
        super().__init__(message, details)
        self.filename = filename


class InvalidPositionError(GameError):
    """Невірна позиція"""
    
    def __init__(self, message: str = "Невірна позиція", position: Optional[tuple] = None) -> None:
        details = f"Позиція: {position}" if position else None
        super().__init__(message, details)
        self.position = position
