import os
from typing import Any, Collection, Set, cast

import pytest
import requests
from pytest import MonkeyPatch
from pytest_mock.plugin import MockerFixture
from us_congress._exceptions import NoCongressApiKeyException
from us_congress.congress import Congress

from tests.integration.congress.mockApi import MOCK_CONGRESS_API
from tests.serviceTestFixtures import ServiceTestFixture
from tests.utils import MockRes


@pytest.fixture(scope="function", autouse=True)
def apiCalls(monkeypatch: MonkeyPatch) -> Set[str]:
    _apiCalls: Set[str] = set()

    def mockGet(route: str, **kwargs: Any):
        _apiCalls.add(route)
        res = cast(Collection[Any], MOCK_CONGRESS_API.get(route))
        status_code = 404 if res is None else 200
        return MockRes(status_code, res)

    monkeypatch.setattr(requests, "get", mockGet)

    return _apiCalls


@pytest.fixture(autouse=True)
def givenEnvVar(mocker: MockerFixture):
    mocker.patch.object(os, "getenv", return_value="banana")


class DummyClass:
    def __init__(self) -> None:
        super().__init__()


@pytest.mark.integration
class TestCongress(ServiceTestFixture[DummyClass]):
    def test_Congress_givenNoApiKey_throws(self):
        self.mocker.patch.object(os, "getenv", return_value=None)

        with pytest.raises(
            NoCongressApiKeyException,
            match="Could not find `PROPUBLICA_CONG_KEY in .env",
        ):
            _ = Congress(116)

    def test_getSenators(self):
        congress = Congress(116)

        senators = congress.getSenators()

        assert senators.to_dict("records") == [
            {
                "fips": "47",
                "firstName": "Lamar",
                "id": "A000360",
                "lastName": "Alexander",
                "middleName": None,
                "party": "R",
                "percents_missedVotes": 18.55,
                "percents_votesAgainstParty": 3.45,
                "percents_votesWithParty": 96.55,
                "shortTitle": "Sen.",
                "state": "TN",
                "suffix": None,
                "title": "Senator, 2nd Class",
                "votes_missed": 133,
                "votes_present": 0,
                "votes_total": 717,
            },
            {
                "fips": "55",
                "firstName": "Tammy",
                "id": "B001230",
                "lastName": "Baldwin",
                "middleName": None,
                "party": "D",
                "percents_missedVotes": 0.28,
                "percents_votesAgainstParty": 5.35,
                "percents_votesWithParty": 94.65,
                "shortTitle": "Sen.",
                "state": "WI",
                "suffix": None,
                "title": "Senator, 1st Class",
                "votes_missed": 2,
                "votes_present": 1,
                "votes_total": 717,
            },
        ]

    def test_getRepresentatives(self):
        congress = Congress(116)

        senators = congress.getRepresentatives()

        assert senators.to_dict("records") == [
            {
                "district": "05",
                "fips": "22",
                "firstName": "Ralph",
                "id": "A000374",
                "lastName": "Abraham",
                "middleName": None,
                "party": "R",
                "percents_missedVotes": 39.52,
                "percents_votesAgainstParty": 4.9,
                "percents_votesWithParty": 94.93,
                "shortTitle": "Rep.",
                "state": "LA",
                "suffix": None,
                "title": "Representative",
                "votes_missed": 377,
                "votes_present": 0,
                "votes_total": 954,
            },
            {
                "district": "12",
                "fips": "37",
                "firstName": "Alma",
                "id": "A000370",
                "lastName": "Adams",
                "middleName": None,
                "party": "D",
                "percents_missedVotes": 2.73,
                "percents_votesAgainstParty": 0.65,
                "percents_votesWithParty": 99.24,
                "shortTitle": "Rep.",
                "state": "NC",
                "suffix": None,
                "title": "Representative",
                "votes_missed": 26,
                "votes_present": 0,
                "votes_total": 954,
            },
        ]

    def test_repr(self):
        cong = Congress(116)

        assert str(cong) == "<Congress 116>"
