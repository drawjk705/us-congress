from abc import ABC, abstractmethod
from typing import List

from congress._api.models import Representative, Senator


class ICongressApiFetchService(ABC):
    """
    Calls ProPublica API to get basic
    info on congressional leaders
    """

    @abstractmethod
    def getRepresentatives(self) -> List[Representative]:
        ...

    @abstractmethod
    def getSenators(self) -> List[Senator]:
        pass
