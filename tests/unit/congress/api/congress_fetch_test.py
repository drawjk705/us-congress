from typing import Any, Dict

from congress._api.fetch import CongressApiFetchService
from congress._api.models import Congressman, Representative, Senator
from congress._config import CongressConfig
from tests.serviceTestFixtures import ApiServiceTestFixture
from tests.utils import MockRes

apiKey = "apiKey"
config = CongressConfig(116, apiKey)

repsRetval: Dict[str, Any] = {
    "results": [
        {
            "members": [
                dict(
                    id="abc123",
                    title="Mister",
                    short_title="Mr.",
                    first_name="Bob",
                    middle_name="D.",
                    last_name="Jones",
                    suffix="III",
                    party="R",
                    state="NY",
                    district="123",
                    missed_vote_pct=10,
                    votes_with_party_pct=20,
                    votes_against_party_pcy=70,
                    total_votes=10,
                    missed_votes=2,
                    total_present=3,
                ),
                dict(
                    id="def456",
                    title="Madam",
                    short_title="Mm.",
                    first_name="Shirley",
                    middle_name="Q.",
                    last_name="Dirkstein",
                    suffix="Esq.",
                    party="D",
                    state="NY",
                    district="133",
                    missed_vote_pct=13,
                    votes_with_party_pct=10,
                    votes_against_party_pcy=67,
                    total_votes=3,
                    missed_votes=5,
                    total_present=6,
                ),
            ]
        }
    ]
}

sensRetval: Dict[str, Any] = {
    "results": [
        {
            "members": [
                dict(
                    id="abc123",
                    title="Mister",
                    short_title="Mr.",
                    first_name="Bob",
                    middle_name="D.",
                    last_name="Jones",
                    suffix="III",
                    party="R",
                    state="NY",
                    missed_vote_pct=10,
                    votes_with_party_pct=20,
                    votes_against_party_pcy=70,
                    total_votes=10,
                    missed_votes=2,
                    total_present=3,
                ),
                dict(
                    id="def456",
                    title="Madam",
                    short_title="Mm.",
                    first_name="Shirley",
                    middle_name="Q.",
                    last_name="Dirkstein",
                    suffix="Esq.",
                    party="D",
                    state="NY",
                    missed_vote_pct=13,
                    votes_with_party_pct=10,
                    votes_against_party_pcy=67,
                    total_votes=3,
                    missed_votes=5,
                    total_present=6,
                ),
            ]
        }
    ]
}


class ApiWrapper(CongressApiFetchService):
    def __init__(self) -> None:
        super().__init__(config)


class TestCongressApiFetch(ApiServiceTestFixture[ApiWrapper]):
    def test_getRepresentatives_callsCorrectEndpoint(self):
        _ = self._service.getRepresentatives()

        self.requestsGetMock.assert_called_once_with(
            "https://api.propublica.org/congress/v1/116/house/members.json",
            headers={"X-API-Key": "apiKey"},
        )

    def test_getRepresentatives_parsesResponse(self):
        self.requestsGetMock.return_value = MockRes(200, repsRetval)

        res = self._service.getRepresentatives()

        assert res == [
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

    def test_getSenators_callsCorrectEndpoint(self):
        _ = self._service.getSenators()

        self.requestsGetMock.assert_called_once_with(
            "https://api.propublica.org/congress/v1/116/senate/members.json",
            headers={"X-API-Key": "apiKey"},
        )

    def test_getSenators_parsesResponse(self):
        self.requestsGetMock.return_value = MockRes(200, sensRetval)

        res = self._service.getSenators()

        assert res == [
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
