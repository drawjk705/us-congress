from typing import Generator, List, TypeVar

_T = TypeVar("_T")


def chunk(items: List[_T], n: int) -> Generator[List[_T], None, None]:
    """
    Splits a list into `n`-sized chunks

    Args:
        items (List[_T]): the list
        n (int): the chunk size

    Yields:
        Generator[List[_T], None, None]: Generator of each chunk
    """
    for i in range(0, len(items), n):
        yield items[i : i + n]
