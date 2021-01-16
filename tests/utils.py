from itertools import product
from typing import Any, Collection, List, Tuple

import pandas
from callee.base import Matcher


class ServiceTestFixtureException(Exception):
    pass


class _RequestCls:
    class Obj:
        serviceType: Any
        _service: Any
        _dependencies: Any

    cls: Obj


def extractService(obj: _RequestCls.Obj) -> Any:
    """
    This is some clever hackery to get the class type
    of the TypeVar that we pass in to `ServiceTestFixture`.
    So if we create a test suite such as:

    ```python
    class Suite(ServiceTestFixture[MyService]):
        pass
    ```

    this function will get the class type of `MyService`,
    as opposed to just treating `MyService` like a generic
    type.

    Args:
        obj (_RequestCls.Obj): Instance of the test suite
        retrieved with pytest

    Raises:
        ServiceTestFixtureException

    Returns:
        The class type of the service in question
    """

    # this lets us get the class that our test fixture
    # is inheriting from (i.e., ServiceTestFixture[T])
    fixtureClass = [
        base
        for base in obj.__dict__["__orig_bases__"]
        if "ServiceTestFixture[" in str(base)
    ]
    if len(fixtureClass) != 1:
        raise ServiceTestFixtureException(
            "Test Suite is inheriting from more than one class"
        )

    fixtureClass = fixtureClass[0]

    # here, we try to extract the class type of the
    # type argument passed in (the `T`) in `ServiceTestFixture[T]`
    if not hasattr(fixtureClass, "__args__"):
        raise ServiceTestFixtureException(
            "ServiceTestFixture does not have any type arguments"
        )

    if len(fixtureClass.__args__) != 1:  # type: ignore
        raise ServiceTestFixtureException("ServiceTestFixture needs one type argument")

    return fixtureClass.__args__[0]  # type: ignore


def shuffledCases(**kwargs: List[Any]) -> Tuple[List[str], List[Any]]:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    combos = list(product(*values))

    return keys, combos


class DataFrameColumnMatcher(Matcher):
    _columnsValues: List[str]
    _columnToMatch: str

    def __init__(self, columnsValues: List[str], columnToMatch: str) -> None:
        self._columnsValues = columnsValues
        self._columnToMatch = columnToMatch

    def match(self, value: Any):
        if not isinstance(value, pandas.DataFrame):
            return False
        values = value[self._columnToMatch].tolist()  # type: ignore
        return self._columnsValues == values


class MockRes:
    status_code: int
    content: Collection[Any]

    def __init__(self, status_code: int, content: Collection[Any] = {}) -> None:
        self.status_code = status_code
        self.content = content

    def json(self) -> Collection[Any]:
        if self.status_code != 200:
            raise Exception("uh oh")

        return self.content
