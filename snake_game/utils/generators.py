# Генератори для гри

from typing import Generator, Tuple, List
import os


def level_parser(filename: str) -> Generator[Tuple[int, int, List[List[str]]], None, None]:
    """Генератор для завантаження рівнів з файлу"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            
            if not lines or not lines[0].strip():
                continue
            if lines[0].strip().startswith('#'):
                continue
            
            try:
                parts = lines[0].split()
                if len(parts) != 2:
                    continue
                
                w, h = int(parts[0]), int(parts[1])
                
                matrix = []
                for i in range(1, min(len(lines), h + 1)):
                    row = list(lines[i])
                    while len(row) < w:
                        row.append(' ')
                    matrix.append(row[:w])
                
                if len(matrix) == h:
                    yield (w, h, matrix)
                    
            except (ValueError, IndexError):
                continue
                
    except FileNotFoundError:
        return


def highscore_reader(filename: str, limit: int = 5) -> Generator[Tuple[int, str, str], None, None]:
    """Генератор для читання рекордів з файлу"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            count = 0
            for line in f:
                if count >= limit:
                    break
                
                parts = line.strip().split('|')
                if len(parts) == 3:
                    score, name, date = parts
                    yield (int(score), name, date)
                    count += 1
                    
    except FileNotFoundError:
        return


def spiral_positions(center_x: int, center_y: int, max_radius: int) -> Generator[Tuple[int, int], None, None]:
    """Генератор позицій по спіралі від центру"""
    yield (center_x, center_y)
    
    for radius in range(1, max_radius + 1):
        # Верхня грань
        for x in range(center_x - radius, center_x + radius + 1):
            yield (x, center_y - radius)
        
        # Права грань
        for y in range(center_y - radius + 1, center_y + radius):
            yield (center_x + radius, y)
        
        # Нижня грань
        for x in range(center_x + radius, center_x - radius - 1, -1):
            yield (x, center_y + radius)
        
        # Ліва грань
        for y in range(center_y + radius - 1, center_y - radius, -1):
            yield (center_x - radius, y)


def fibonacci(limit: int = 10) -> Generator[int, None, None]:
    """Послідовність Фібоначчі"""
    a, b = 0, 1
    count = 0
    
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1


def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """Нескінченний лічильник"""
    current = start
    while True:
        yield current
        current += step


def batch_iterator(items: List[any], batch_size: int) -> Generator[List[any], None, None]:
    """Генератор для розбиття списку на партії"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
