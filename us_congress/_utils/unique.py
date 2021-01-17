from typing import Collection, List, Set, TypeVar

T = TypeVar("T")


def getUnique(items: Collection[T]) -> List[T]:
    """
    Get all unique elements in a list

    Args:
        items (List[T])

    Returns:
        List[T]: list with distinct items
    """

    uniqueList: List[T] = []
    seenItems: Set[T] = set()

    for item in items:
        if item in seenItems:
            continue
        seenItems.add(item)
        uniqueList.append(item)

    return uniqueList
