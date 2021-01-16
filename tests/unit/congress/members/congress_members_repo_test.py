from unittest.mock import MagicMock

from congress._members.service import CongressMemberRepository
from tests.serviceTestFixtures import ServiceTestFixture


class TestCongressMembersRepository(ServiceTestFixture[CongressMemberRepository]):
    def test_getRepresentatives(self):
        apiRetval = MagicMock()
        apiGet = self.mocker.patch.object(
            self._service._api, "getRepresentatives", return_value=apiRetval
        )

        _ = self._service.getRepresentatives()

        apiGet.assert_called_once()
        self.castMock(self._service._api.getRepresentatives).assert_called_once()
        self.castMock(
            self._service._transformer.congressmembers
        ).assert_called_once_with(apiRetval)

    def test_getSenators(self):
        apiRetval = MagicMock()
        apiGet = self.mocker.patch.object(
            self._service._api, "getSenators", return_value=apiRetval
        )

        _ = self._service.getSenators()

        apiGet.assert_called_once()
        self.castMock(self._service._api.getSenators).assert_called_once()
        self.castMock(
            self._service._transformer.congressmembers
        ).assert_called_once_with(apiRetval)
