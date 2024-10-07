from pageobjects.text.fill_form import FillForm


class TestFillForm:

    def test_fill_user(self, make_driver):
        fill = FillForm(make_driver)
        fill.enter_username("selenium framework")
