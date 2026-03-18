import allure


@allure.step("Сравнить {result} и {expected_result}")
def assertion_is_equals(result, expected_result):
    assert result == expected_result, f"{result} не равно {expected_result}"


@allure.step("Проверить что {value} присутствует в {values_list}")
def assertion_in(value, values_list):
    assert value in values_list, f"{value} отсутствует в {values_list}"


@allure.step("Проверить что {result} отсутствует в {results_list}")
def assertion_is_not_equals_in_list(result, results_list):
    for item_list in results_list:
        assert result != item_list
