class TestMain(object):
    def test_main(self, make_driver):
        make_driver

    def test_main3(self, make_driver):
        make_driver

    def test_main4(self, make_driver):
        make_driver

    def test_main5(self, make_driver):
        make_driver

    def test_main6(self, make_driver):
        make_driver

    def test_example(self, make_driver):
        driver = make_driver
        assert driver.title == "Example sad as Domain"  # This will fail to demonstrate screenshot capture
