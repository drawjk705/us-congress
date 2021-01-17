import logging
from typing import cast
from unittest.mock import MagicMock

from pytest_mock import MockerFixture
from us_congress._utils.chunk import chunk
from us_congress._utils.timer import timer
from us_congress._utils.unique import getUnique


def test_chunk_givenChunkLessThanSize():
    items = [1, 2, 3, 4]
    n = 2

    for i, subset in enumerate(chunk(items, n)):
        if i == 0:
            assert subset == [1, 2]
        elif i == 1:
            assert subset == [3, 4]


def test_chunk_givenChunkGreaterThanSize():
    items = [1, 2, 3, 4]
    n = 5

    for i, subset in enumerate(chunk(items, n)):
        assert i == 0
        assert subset == items


def test_getUnique_preservesOrder():
    items = [1, 2, 3, 4, 5, 1]

    res = getUnique(items)

    assert res == [1, 2, 3, 4, 5]


def test_timer_logsAndReturnsValues(mocker: MockerFixture):
    @timer
    def fn() -> int:
        return 1

    mockLogging = mocker.patch("us_congress._utils.timer.logging")
    mockLogger = MagicMock()
    cast(MagicMock, cast(logging, mockLogging).getLogger).return_value = mockLogger
    mockPerfCounter = mocker.patch("us_congress._utils.timer.time")
    mockPerfCounter.perf_counter.side_effect = [1, 2]  # type: ignore

    retval = fn()

    cast(MagicMock, mockLogger.debug).assert_called_once_with(  # type: ignore
        "[test_timer_logsAndReturnsValues.<locals>.fn] - duration: 1000.00ms"
    )
    assert retval == 1
