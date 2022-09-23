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
from .engine_test_configs import Config054
from .engine_test_configs import Config055
from .engine_test_configs import Config056
from .engine_test_configs import Config057
from .engine_test_configs import Config058
from .engine_test_configs import Config059
from .engine_test_configs import Config060
from .engine_test_configs import Config061
from .engine_test_configs import Config062
from .engine_test_configs import Config063
from .engine_test_configs import Config064
from .engine_test_configs import Config065
from .engine_test_configs import Config066
from .engine_test_configs import Config067
from .engine_test_configs import Config068
from .engine_test_configs import Config069
from .engine_test_configs import Config070
from .engine_test_configs import Config071
from .engine_test_configs import Config072
from .engine_test_configs import Config073
from .engine_test_configs import Config074
from .engine_test_configs import Config075
from .engine_test_configs import Config076
from .engine_test_configs import Config077
from .engine_test_configs import Config078
from .engine_test_configs import Config079
from .engine_test_configs import Config080
from .engine_test_configs import Config081
from .engine_test_configs import Config082
from .engine_test_configs import Config083
from .engine_test_configs import Config084
from .engine_test_configs import Config085
from .engine_test_configs import Config086
from .engine_test_configs import Config087
from .engine_test_configs import Config088
from .engine_test_configs import Config089
from .engine_test_configs import Config090


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
                              Config053,
                              Config054,
                              Config055,
                              Config056,
                              Config057,
                              Config058,
                              Config059,
                              Config060,
                              Config061,
                              Config062,
                              Config063,
                              Config064,
                              Config065,
                              Config066,
                              Config067,
                              Config068,
                              Config069,
                              Config070,
                              Config071,
                              Config072,
                              Config073,
                              Config074,
                              Config075,
                              Config076,
                              Config077,
                              Config078,
                              Config079,
                              Config080,
                              Config081,
                              Config082,
                              Config083,
                              Config084,
                              Config085,
                              Config086,
                              Config087,
                              Config088,
                              Config089,
                              Config090])
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
