from utils.properties import Properties


class TestMain(object):
    def test_main(self, make_driver):
        driver = make_driver
        driver.get(Properties.get_base_url('stag'))

    def test_main3(self, make_driver):
        make_driver

    def test_main4(self, make_driver):
        make_driver
