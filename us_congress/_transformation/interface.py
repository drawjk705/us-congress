from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from us_congress._api.models import Congressman


class ICongressDataTransformationService(ABC):
    """
    translates API results into DataFrames
    """

    @abstractmethod
    def congressmembers(self, members: List[Congressman]) -> pd.DataFrame:
        pass
