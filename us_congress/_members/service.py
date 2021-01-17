from functools import cache
from logging import Logger
from typing import List, cast

import pandas as pd
from us_congress._api.interface import ICongressApiFetchService
from us_congress._api.models import Congressman
from us_congress._members.interface import ICongressMemberRepository
from us_congress._transformation.interface import ICongressDataTransformationService
from us_congress._utils.log.factory import ILoggerFactory
from us_congress._utils.timer import timer


class CongressMemberRepository(ICongressMemberRepository):
    _api: ICongressApiFetchService
    _transformer: ICongressDataTransformationService
    _logger: Logger

    def __init__(
        self,
        api: ICongressApiFetchService,
        transformer: ICongressDataTransformationService,
        loggerFactor: ILoggerFactory,
    ) -> None:
        self._api = api
        self._transformer = transformer
        self._logger = loggerFactor.getLogger(__name__)

    @timer
    def getRepresentatives(self) -> pd.DataFrame:
        return self.__getRepresentatives()

    @cache
    def __getRepresentatives(self) -> pd.DataFrame:
        self._logger.debug("getting representatives")
        apiRes = cast(List[Congressman], self._api.getRepresentatives())

        return self._transformer.congressmembers(apiRes)

    @timer
    def getSenators(self) -> pd.DataFrame:
        return self.__getSenators()

    @cache
    def __getSenators(self) -> pd.DataFrame:
        self._logger.debug("getting senators")
        apiRes = cast(List[Congressman], self._api.getSenators())

        return self._transformer.congressmembers(apiRes)
