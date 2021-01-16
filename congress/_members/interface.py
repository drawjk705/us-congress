from abc import ABC, abstractmethod

import pandas as pd


class ICongressMemberRepository(ABC):
    """
    Gets & stores info for congress members
    """

    @abstractmethod
    def getRepresentatives(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def getSenators(self) -> pd.DataFrame:
        ...
