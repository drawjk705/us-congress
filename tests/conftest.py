import inspect
from typing import Dict, cast
from unittest.mock import MagicMock

import pytest
import requests  # type: ignore
from pytest import FixtureRequest, MonkeyPatch
from pytest_mock.plugin import MockerFixture

from tests import utils

# pyright: reportPrivateUsage=false


@pytest.fixture(autouse=True)
def no_requests(monkeypatch: MonkeyPatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture(scope="function")
def apiFixture(request: FixtureRequest, mocker: MockerFixture):
    request.cls.requestsGetMock = mocker.patch.object(requests, "get")  # type: ignore


@pytest.fixture(scope="function")
def injectMockerToClass(request: FixtureRequest, mocker: MockerFixture):
    request.cls.mocker = mocker  # type: ignore


@pytest.fixture(scope="function")
def injectMonkeyPatchToClass(request: FixtureRequest, monkeypatch: MonkeyPatch):
    request.cls.monkeypatch = monkeypatch  # type: ignore


@pytest.fixture(scope="function")
def serviceFixture(request: FixtureRequest):
    req = cast(utils._RequestCls, request)
    obj = req.cls

    service = utils.extractService(obj)

    dependencies: Dict[str, MagicMock] = {}

    # this lets us see all of the service's constructor types
    for depName, depType in inspect.signature(service).parameters.items():
        # this condition will be true if the service inherits
        # from a generic class
        if hasattr(depType.annotation, "__origin__"):
            dependencies.update({depName: MagicMock(depType.annotation.__origin__)})
        else:
            dependencies.update({depName: MagicMock(depType.annotation)})

    # we call the service's constructor with the mocked dependencies
    # and set the test class obj's _service attribute to hold this service
    obj._service = service(**dependencies)
