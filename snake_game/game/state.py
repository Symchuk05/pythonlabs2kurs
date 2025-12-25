# Стан гри

from typing import Optional


class GameState:
    """Управління станом гри (рахунок, швидкість, рівень)"""
    
    def __init__(self) -> None:
        self.__score: int = 0
        self.__high_score: int = 0
        self._speed: float = 0.2
        self._level: int = 1
    
    @property
    def score(self) -> int:
        """Поточний рахунок"""
        return self.__score
    
    @score.setter
    def score(self, value: int) -> None:
        self.__score = value
        if self.__score > self.__high_score:
            self.__high_score = self.__score
    
    @property
    def high_score(self) -> int:
        """Рекорд"""
        return self.__high_score
    
    @property
    def speed(self) -> float:
        """Швидкість гри"""
        return self._speed
    
    @property
    def level(self) -> int:
        """Поточний рівень"""
        return self._level
    
    def add_points(self, points: int) -> None:
        """Додати бали"""
        self.__score += points
        if self.__score > self.__high_score:
            self.__high_score = self.__score
    
    def make_faster(self) -> None:
        """Прискорити гру"""
        self._speed = max(0.05, self._speed - 0.02)
    
    def reset(self, level: int = 1) -> None:
        """Скинути стан гри"""
        self.__score = 0
        self._speed = 0.2
        self._level = level
    
    def __str__(self) -> str:
        return f"Score: {self.__score} | Record: {self.__high_score} | Level: {self._level}"
    
    def __add__(self, points: int) -> 'GameState':
        """Додати бали через оператор +"""
        self.add_points(points)
        return self
