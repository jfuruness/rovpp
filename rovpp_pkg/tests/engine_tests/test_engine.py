from pathlib import Path

import pytest

from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import EngineTestConfig

from .engine_test_configs import Config035
from .engine_test_configs import Config036
from .engine_test_configs import Config037
from .engine_test_configs import Config038
from .engine_test_configs import Config039
from .engine_test_configs import Config040
from .engine_test_configs import Config041
from .engine_test_configs import Config042
from .engine_test_configs import Config043
from .engine_test_configs import Config044
from .engine_test_configs import Config045
from .engine_test_configs import Config046
from .engine_test_configs import Config047
from .engine_test_configs import Config048
from .engine_test_configs import Config049
from .engine_test_configs import Config050
from .engine_test_configs import Config051
from .engine_test_configs import Config052
from .engine_test_configs import Config053


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize("conf",
                             [Config035,
                              Config036,
                              Config037,
                              Config038,
                              Config039,
                              Config040,
                              Config041,
                              Config042,
                              Config043,
                              Config044,
                              Config045,
                              Config046,
                              Config047,
                              Config048,
                              Config049,
                              Config050,
                              Config051,
                              Config052,
                              Config053])
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

        return Path(__file__).parent / "engine_test_outputs"
