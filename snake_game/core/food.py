# Класи їжі

from typing import Union, Tuple
from .position import Position


class Food:
    """Базовий клас їжі"""
    
    def __init__(self, position: Union[Position, Tuple[int, int]]) -> None:
        if isinstance(position, tuple):
            self._position: Position = Position(position[0], position[1])
        else:
            self._position: Position = position
        
        self._points: int = 10
        self._symbol: str = '*'
    
    @property
    def position(self) -> Position:
        """Позиція їжі"""
        return self._position
    
    @property
    def points(self) -> int:
        """Бали за їжу"""
        return self._points
    
    @property
    def symbol(self) -> str:
        """Символ для відображення"""
        return self._symbol
    
    def __str__(self) -> str:
        return f"Food at {self._position} ({self._points} points)"
    
    def __repr__(self) -> str:
        return f"Food(position={repr(self._position)}, points={self._points})"


class NormalFood(Food):
    """Звичайна їжа (10 балів)"""
    
    def __init__(self, position: Union[Position, Tuple[int, int]]) -> None:
        super().__init__(position)
        self._points = 10
        self._symbol = '*'
    
    def __str__(self) -> str:
        return f"NormalFood at {self._position} (+{self._points})"


class BonusFood(Food):
    """Бонусна їжа (25 балів)"""
    
    def __init__(self, position: Union[Position, Tuple[int, int]]) -> None:
        super().__init__(position)
        self._points = 25
        self._symbol = '$'
    
    def __str__(self) -> str:
        return f"BonusFood at {self._position} (+{self._points})"
