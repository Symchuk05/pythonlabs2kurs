# Декоратори для гри

import time
import functools
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])


def timer(func: F) -> F:
    """Вимірювання часу виконання"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"⏱️  '{func.__name__}' виконувався {elapsed:.2f} сек")
        return result
    return cast(F, wrapper)


def validate_position(func: F) -> F:
    """Валідація позиції"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'x' in kwargs and kwargs['x'] < 0:
            raise ValueError(f"X не може бути негативним: {kwargs['x']}")
        if 'y' in kwargs and kwargs['y'] < 0:
            raise ValueError(f"Y не може бути негативним: {kwargs['y']}")
        return func(*args, **kwargs)
    return cast(F, wrapper)


def cache_result(func: F) -> F:
    """Кешування результатів"""
    cache: dict = {}  # Захоплена змінна
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        else:
            print(f"💾 Кеш для {func.__name__}")
        return cache[key]
    return cast(F, wrapper)


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """Повтор при помилці"""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            last_exception = None
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    if attempts < max_attempts:
                        print(f"⚠️  Спроба {attempts} невдала, повтор через {delay}с...")
                        time.sleep(delay)
            
            print(f"❌ Всі {max_attempts} спроби невдалі")
            raise last_exception  # type: ignore
        
        return cast(F, wrapper)
    return decorator


def limit_calls(max_calls: int) -> Callable[[F], F]:
    """Обмеження кількористі викликів"""
    def decorator(func: F) -> F:
        calls = 0  # Захоплена змінна
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal calls
            
            if calls >= max_calls:
                raise RuntimeError(f"'{func.__name__}' перевищив ліміт ({max_calls})")
            
            calls += 1
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    return decorator


def debug_calls(func: F) -> F:
    """Відлагодження викликів"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"🐛 Виклик {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"🐛 {func.__name__} повернув {result!r}")
        return result
    return cast(F, wrapper)


def create_score_tracker() -> tuple:
    """Фабрика функцій для трекінгу балів"""
    scores: list = []  # Захоплена змінна
    
    def add_score(score: int) -> None:
        """Додати бали"""
        nonlocal scores
        scores.append(score)
        print(f"📊 Додано: {score}")
    
    def get_average() -> float:
        """Середнє значення"""
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_all() -> list:
        """Всі бали"""
        return scores[:]
    
    return add_score, get_average, get_all
