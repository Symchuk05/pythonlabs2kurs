# Ігрове поле

import os
from typing import List, Tuple, Dict, Optional
from .position import Position
from .snake import Snake
from .food import Food


class GameField:
    """Ігрове поле з перешкодами"""
    
    def __init__(self, width: int, height: int, obstacles: Optional[List[List[str]]] = None) -> None:
        self._width: int = width
        self._height: int = height
        
        self._symbols: Dict[str, str] = {
            'head': 'O',
            'body': 'o',
            'wall': '#',
            'empty': ' '
        }
        
        self.__obstacles: List[List[str]] = obstacles if obstacles else self._create_empty_matrix()
    
    @property
    def width(self) -> int:
        """Ширина поля"""
        return self._width
    
    @property
    def height(self) -> int:
        """Висота поля"""
        return self._height
    
    def _create_empty_matrix(self) -> List[List[str]]:
        """Створити порожню матрицю зі стінами"""
        matrix = [
            [self._symbols['wall'] if x == 0 or x == self._width-1 or y == 0 or y == self._height-1
             else self._symbols['empty']
             for x in range(self._width)]
            for y in range(self._height)
        ]
        return matrix
    
    def is_obstacle(self, position: Position) -> bool:
        """Перевірка перешкоди"""
        x, y = position.x, position.y
        
        if y < 0 or y >= self._height or x < 0 or x >= self._width:
            return True
        
        return self.__obstacles[y][x] == self._symbols['wall']
    
    def get_free_cells(self, snake: Snake) -> List[Tuple[int, int]]:
        """Отримати вільні клітинки"""
        free_cells = [
            (x, y)
            for y in range(1, self._height-1)
            for x in range(1, self._width-1)
            if self.__obstacles[y][x] == self._symbols['empty'] 
               and Position(x, y) not in snake
        ]
        return free_cells
    
    def draw(self, snake: Snake, food: Food) -> None:
        """Намалювати поле"""
        os.system('cls')
        
        display = [row[:] for row in self.__obstacles]
        
        # Розмістити їжу
        fx, fy = food.position.x, food.position.y
        display[fy][fx] = food.symbol
        
        # Розмістити змійку
        for i, pos in enumerate(snake):
            symbol = self._symbols['head'] if i == 0 else self._symbols['body']
            display[pos.y][pos.x] = symbol
        
        # Вивести
        for row in display:
            print(''.join(row))
