from typing import List, cast

from us_congress._api.models import Congressman, Representative, Senator
from us_congress._transformation.service import CongressDataTransformationService
from tests.serviceTestFixtures import ServiceTestFixture

representatives = [
    Representative(
        id="abc123",
        title="Mister",
        shortTitle="Mr.",
        firstName="Bob",
        middleName="D.",
        lastName="Jones",
        suffix="III",
        party="R",
        state="NY",
        percents=Congressman._Percents(
            missedVotes=0, votesWithParty=20, votesAgainstParty=0
        ),
        votes=Congressman._Votes(total=10, missed=2, present=3),
        district="123",
    ),
    Representative(
        id="def456",
        title="Madam",
        shortTitle="Mm.",
        firstName="Shirley",
        middleName="Q.",
        lastName="Dirkstein",
        suffix="Esq.",
        party="D",
        state="NY",
        percents=Congressman._Percents(
            missedVotes=0, votesWithParty=10, votesAgainstParty=0
        ),
        votes=Congressman._Votes(total=3, missed=5, present=6),
        district="133",
    ),
]
senators = [
    Senator(
        id="abc123",
        title="Mister",
        shortTitle="Mr.",
        firstName="Bob",
        middleName="D.",
        lastName="Jones",
        suffix="III",
        party="R",
        state="NY",
        percents=Congressman._Percents(
            missedVotes=0, votesWithParty=20, votesAgainstParty=0
        ),
        votes=Congressman._Votes(total=10, missed=2, present=3),
    ),
    Senator(
        id="def456",
        title="Madam",
        shortTitle="Mm.",
        firstName="Shirley",
        middleName="Q.",
        lastName="Dirkstein",
        suffix="Esq.",
        party="D",
        state="NY",
        percents=Congressman._Percents(
            missedVotes=0, votesWithParty=10, votesAgainstParty=0
        ),
        votes=Congressman._Votes(total=3, missed=5, present=6),
    ),
]


class TestCongressDataTransformationService(
    ServiceTestFixture[CongressDataTransformationService]
):
    def test_congressmembers_givenRepresentatives(self):
        res = self._service.congressmembers(cast(List[Congressman], representatives))

        assert res.to_dict("records") == [
            {
                "district": "123",
                "fips": "36",
                "firstName": "Bob",
                "id": "abc123",
                "lastName": "Jones",
                "middleName": "D.",
                "party": "R",
                "percents_missedVotes": 0,
                "percents_votesAgainstParty": 0,
                "percents_votesWithParty": 20,
                "shortTitle": "Mr.",
                "state": "NY",
                "suffix": "III",
                "title": "Mister",
                "votes_missed": 2,
                "votes_present": 3,
                "votes_total": 10,
            },
            {
                "district": "133",
                "fips": "36",
                "firstName": "Shirley",
                "id": "def456",
                "lastName": "Dirkstein",
                "middleName": "Q.",
                "party": "D",
                "percents_missedVotes": 0,
                "percents_votesAgainstParty": 0,
                "percents_votesWithParty": 10,
                "shortTitle": "Mm.",
                "state": "NY",
                "suffix": "Esq.",
                "title": "Madam",
                "votes_missed": 5,
                "votes_present": 6,
                "votes_total": 3,
            },
        ]

    def test_congressmembers_givenSenators(self):
        res = self._service.congressmembers(cast(List[Congressman], senators))

        assert res.to_dict("records") == [
            {
                "fips": "36",
                "firstName": "Bob",
                "id": "abc123",
                "lastName": "Jones",
                "middleName": "D.",
                "party": "R",
                "percents_missedVotes": 0,
                "percents_votesAgainstParty": 0,
                "percents_votesWithParty": 20,
                "shortTitle": "Mr.",
                "state": "NY",
                "suffix": "III",
                "title": "Mister",
                "votes_missed": 2,
                "votes_present": 3,
                "votes_total": 10,
            },
            {
                "fips": "36",
                "firstName": "Shirley",
                "id": "def456",
                "lastName": "Dirkstein",
                "middleName": "Q.",
                "party": "D",
                "percents_missedVotes": 0,
                "percents_votesAgainstParty": 0,
                "percents_votesWithParty": 10,
                "shortTitle": "Mm.",
                "state": "NY",
                "suffix": "Esq.",
                "title": "Madam",
                "votes_missed": 5,
                "votes_present": 6,
                "votes_total": 3,
            },
        ]
