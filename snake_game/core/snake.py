# Клас змійки

from typing import List, Tuple, Union, Iterator, Set
from .position import Position


class Snake:
    """Змійка гравця з протоколом послідовності"""
    
    def __init__(self, initial_positions: List[Union[Position, Tuple[int, int]]]) -> None:
        self.__body: List[Position] = []
        for pos in initial_positions:
            if isinstance(pos, tuple):
                self.__body.append(Position(pos[0], pos[1]))
            else:
                self.__body.append(pos)
        
        self._direction: str = 'RIGHT'
        self._visited_cells: Set[Tuple[int, int]] = set()
    
    @property
    def head(self) -> Position:
        """Голова змійки"""
        return self.__body[0]
    
    @property
    def body(self) -> List[Position]:
        """Копія тіла змійки"""
        return self.__body[:]
    
    @property
    def direction(self) -> str:
        """Поточний напрямок"""
        return self._direction
    
    @direction.setter
    def direction(self, value: str) -> None:
        """Встановити напрямок (з перевіркою протилежного)"""
        opposites = {
            'UP': 'DOWN', 'DOWN': 'UP',
            'LEFT': 'RIGHT', 'RIGHT': 'LEFT'
        }
        if opposites.get(self._direction) != value:
            self._direction = value
    
    def __len__(self) -> int:
        """Довжина змійки"""
        return len(self.__body)
    
    def __str__(self) -> str:
        return f"Snake(length={len(self.__body)}, head={self.head})"
    
    def __repr__(self) -> str:
        return f"Snake(positions={len(self.__body)}, dir='{self._direction}')"
    
    def __contains__(self, position: Union[Position, Tuple[int, int]]) -> bool:
        """Перевірка наявності позиції в змійці"""
        return position in self.__body
    
    def __getitem__(self, index: int) -> Position:
        """Доступ до сегмента за індексом"""
        return self.__body[index]
    
    def __iter__(self) -> Iterator[Position]:
        """Ітерація по змійці"""
        return iter(self.__body)
    
    def __reversed__(self) -> Iterator[Position]:
        """Зворотна ітерація"""
        return reversed(self.__body)
    
    def move(self, grow: bool = False) -> None:
        """Рух змійки"""
        new_head = self.head.move(self._direction)
        self.__body.insert(0, new_head)
        self._visited_cells.add((new_head.x, new_head.y))
        
        if not grow:
            self.__body.pop()
    
    def check_collision(self) -> bool:
        """Перевірка зіткнення з собою"""
        return self.head in self.__body[1:]
    
    def get_visited_count(self) -> int:
        """Кількість відвіданих клітинок"""
        return len(self._visited_cells)
