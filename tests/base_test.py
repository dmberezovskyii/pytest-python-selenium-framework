import pytest


@pytest.mark.usefixtures("make_driver")
class BaseTestCase:
    pass
