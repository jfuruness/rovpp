import pytest


class Unstable:
    @pytest.mark.skip(reason=("ROV++ can't handle multi round propagation"
                              " due to the way we count holes"))
    def test_stable(*args, **kwargs):
        pass
