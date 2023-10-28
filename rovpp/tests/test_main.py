import pytest

from ..__main__ import main


@pytest.mark.slow
@pytest.mark.skip(reason="Takes 10m, not worth it")
class TestMain:
    def test_main(self):
        """Runs through the graphs quickly, simple sanity check"""

        main(quick=True)
