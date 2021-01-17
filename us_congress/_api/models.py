from abc import abstractclassmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Congressman:
    @dataclass(frozen=True)
    class _Percents:
        missedVotes: float
        votesWithParty: float
        votesAgainstParty: float

    @dataclass(frozen=True)
    class _Votes:
        total: int
        missed: int
        present: int

    id: str
    title: str
    shortTitle: str
    firstName: str
    middleName: str
    lastName: str
    suffix: str
    party: str
    state: str
    percents: _Percents
    votes: _Votes

    @staticmethod
    def _getPercents(jsonRes: Dict[str, Any]) -> _Percents:
        return Congressman._Percents(
            missedVotes=jsonRes.get("missed_votes_pct") or 0,
            votesWithParty=jsonRes.get("votes_with_party_pct") or 0,
            votesAgainstParty=jsonRes.get("votes_against_party_pct") or 0,
        )

    @staticmethod
    def _getVotes(jsonRes: Dict[str, Any]) -> _Votes:
        return Congressman._Votes(
            total=jsonRes.get("total_votes") or 0,
            missed=jsonRes.get("missed_votes") or 0,
            present=jsonRes.get("total_present") or 0,
        )

    @abstractclassmethod
    def fromJson(cls, jsonRes: Dict[str, Any]) -> Any:
        ...


@dataclass(frozen=True)
class Representative(Congressman):
    district: str

    @classmethod
    def fromJson(cls, jsonRes: Dict[str, Any]):
        percents = Congressman._getPercents(jsonRes)
        votes = Congressman._getVotes(jsonRes)

        return cls(
            id=jsonRes["id"],
            title=jsonRes["title"],
            shortTitle=jsonRes["short_title"],
            firstName=jsonRes["first_name"],
            middleName=jsonRes["middle_name"],
            lastName=jsonRes["last_name"],
            suffix=jsonRes["suffix"],
            party=jsonRes["party"],
            state=jsonRes["state"],
            district=jsonRes["district"],
            percents=percents,
            votes=votes,
        )


@dataclass(frozen=True)
class Senator(Congressman):
    @classmethod
    def fromJson(cls, jsonRes: Dict[str, Any]):
        percents = Congressman._getPercents(jsonRes)
        votes = Congressman._getVotes(jsonRes)

        return cls(
            id=jsonRes["id"],
            title=jsonRes["title"],
            shortTitle=jsonRes["short_title"],
            firstName=jsonRes["first_name"],
            middleName=jsonRes["middle_name"],
            lastName=jsonRes["last_name"],
            suffix=jsonRes["suffix"],
            party=jsonRes["party"],
            state=jsonRes["state"],
            percents=percents,
            votes=votes,
        )
