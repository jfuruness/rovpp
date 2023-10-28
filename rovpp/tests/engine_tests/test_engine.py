from pathlib import Path

import pytest

from bgpy import EngineTester
from bgpy import EngineTestConfig
from bgpy import engine_test_configs as bgpy_engine_test_configs

from .engine_test_configs import engine_test_configs


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize("conf", bgpy_engine_test_configs + engine_test_configs)
    def test_engine(self, conf: EngineTestConfig, overwrite: bool):
        """Performs a system test on the engine

        See README for in depth details
        """

        EngineTester(
            base_dir=self.base_dir, conf=conf, overwrite=overwrite
        ).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "engine_test_outputs"
