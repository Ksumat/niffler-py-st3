import pytest


class Pages:
    open_main_page = pytest.mark.usefixtures("open_main_page")
    open_spending_page = pytest.mark.usefixtures("open_spending_page")
    open_login_page = pytest.mark.usefixtures("open_login_page")
    open_profile_page = pytest.mark.usefixtures("open_profile_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])
