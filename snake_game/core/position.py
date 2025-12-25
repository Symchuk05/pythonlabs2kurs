# Клас позиції на полі

from typing import Tuple, Dict


class Position:
    """Позиція на ігровому полі"""
    
    def __init__(self, x: int, y: int) -> None:
        self.__x: int = x  # Приватний атрибут
        self.__y: int = y
    
    @property
    def x(self) -> int:
        """Координата X"""
        return self.__x
    
    @property
    def y(self) -> int:
        """Координата Y"""
        return self.__y
    
    def __eq__(self, other: object) -> bool:
        """Порівняння позицій"""
        if isinstance(other, Position):
            return self.__x == other.__x and self.__y == other.__y
        elif isinstance(other, tuple) and len(other) == 2:
            return self.__x == other[0] and self.__y == other[1]
        return False
    
    def __hash__(self) -> int:
        """Хеш для множин"""
        return hash((self.__x, self.__y))
    
    def __str__(self) -> str:
        """Строкове представлення"""
        return f"({self.__x}, {self.__y})"
    
    def __repr__(self) -> str:
        """Формальне представлення"""
        return f"Position({self.__x}, {self.__y})"
    
    def to_tuple(self) -> Tuple[int, int]:
        """Конвертація в кортеж"""
        return (self.__x, self.__y)
    
    def move(self, direction: str) -> 'Position':
        """Новапозиція після руху"""
        moves: Dict[str, Tuple[int, int]] = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        dx, dy = moves.get(direction, (0, 0))
        return Position(self.__x + dx, self.__y + dy)
