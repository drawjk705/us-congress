from typing import Any, Dict, List, cast

import requests
from us_congress._api.interface import ICongressApiFetchService
from us_congress._api.models import Representative, Senator
from us_congress._config import CongressConfig

BASE_URL = "https://api.propublica.org/congress/v1"


class CongressApiFetchService(ICongressApiFetchService):
    _config: CongressConfig

    def __init__(self, config: CongressConfig) -> None:
        self._config = config

    def getRepresentatives(self) -> List[Representative]:
        res = self.__fetch("house/members.json")
        members = cast(List[Dict[str, Any]], res["results"][0]["members"])

        return [Representative.fromJson(member) for member in members]

    def getSenators(self) -> List[Senator]:
        res = self.__fetch("senate/members.json")
        members = cast(List[Dict[str, Any]], res["results"][0]["members"])

        return [Senator.fromJson(member) for member in members]

    def __fetch(self, path: str) -> Any:
        headers: Dict[str, str] = {"X-API-Key": self._config.apiKey}

        return requests.get(f"{BASE_URL}/{self._config.congress}/{path}", headers=headers).json()  # type: ignore
