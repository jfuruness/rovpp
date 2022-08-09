import pytest

from bgp_simulator_pkg import pytest_addoption as bgp_simulator_addoption

# https://stackoverflow.com/a/66597438/8903959
def pytest_addoption(parser):
    bgp_simulator_addoption(parser)
