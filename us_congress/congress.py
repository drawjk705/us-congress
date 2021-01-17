# pyright: reportUnknownMemberType=false

import os
from typing import cast

import dotenv
import pandas
import punq
from us_congress._api.fetch import CongressApiFetchService
from us_congress._api.interface import ICongressApiFetchService
from us_congress._client import CongressClient
from us_congress._config import CongressConfig
from us_congress._exceptions import NoCongressApiKeyException
from us_congress._members.interface import ICongressMemberRepository
from us_congress._members.service import CongressMemberRepository
from us_congress._transformation.interface import ICongressDataTransformationService
from us_congress._transformation.service import CongressDataTransformationService
from us_congress._utils.log.configureLogger import DEFAULT_LOGFILE, configureLogger
from us_congress._utils.log.factory import ILoggerFactory, LoggerFactory

_transformer = CongressDataTransformationService()
_loggerFactory = LoggerFactory()


class Congress:
    _client: CongressClient
    _config: CongressConfig

    def __init__(self, congressNumber: int, logFile: str = DEFAULT_LOGFILE) -> None:
        dotenvPath = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenvPath)  # type: ignore

        apiKey = os.getenv("PROPUBLICA_CONG_KEY")

        if apiKey is None:
            raise NoCongressApiKeyException(
                "Could not find `PROPUBLICA_CONG_KEY in .env"
            )

        self._config = CongressConfig(congressNumber, apiKey)

        container = punq.Container()

        # singletons
        container.register(ICongressDataTransformationService, instance=_transformer)
        container.register(CongressConfig, instance=self._config)
        container.register(ILoggerFactory, instance=_loggerFactory)

        container.register(ICongressApiFetchService, CongressApiFetchService)
        container.register(ICongressMemberRepository, CongressMemberRepository)

        container.register(CongressClient)

        configureLogger(logFile)

        self._client = cast(CongressClient, container.resolve(CongressClient))

    def getSenators(self) -> pandas.DataFrame:
        return self._client.getSenators().copy(deep=True)

    def getRepresentatives(self) -> pandas.DataFrame:
        return self._client.getRepresentatives().copy(deep=True)

    def __repr__(self) -> str:
        return f"<Congress {self._config.congress}>"
