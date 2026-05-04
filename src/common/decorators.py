import time
from functools import wraps


def measure_time(func):
    """Декоратор для вычисления скорости работы функции"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()

        print(f"Время выполнения {func.__name__}: {(end - start) * 1000} мс")
        return result
    return wrapper
