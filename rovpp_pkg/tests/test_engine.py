from pathlib import Path

import pytest

from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import EngineTestConfig

from .system_tests import Config035

@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize("conf",
                             [Config035])
    def test_engine(self, conf: EngineTestConfig, overwrite: bool):
        """Performs a system test on the engine

        See README for in depth details
        """

        EngineTester(base_dir=self.base_dir,
                     conf=conf,
                     overwrite=overwrite).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "system_test_outputs"
