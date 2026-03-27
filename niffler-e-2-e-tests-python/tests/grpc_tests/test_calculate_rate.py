import grpc
import pytest
import allure

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues


@allure.story('Конвертер валют')
@allure.feature('grpc')
class TestRate:

    @allure.title('Конвертация EUR в RUB')
    def test_calculate_rate(self, grpc_client: NifflerCurrencyServiceClient):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                desiredCurrency=CurrencyValues.RUB,
                amount=100
            )
        )
        assert response.calculatedAmount == 7200, "Expected 7200"

    @allure.title('Конвертация без указания валюты')
    def test_calculate_rate_without_desired_currency(self, grpc_client: NifflerCurrencyServiceClient):
        try:
            grpc_client.calculate_rate(
                request=CalculateRequest(
                    spendCurrency=CurrencyValues.EUR,
                    amount=100
                )
            )
        except grpc.RpcError as e:
            assert e.code() == grpc.StatusCode.UNKNOWN
            assert e.details() == "Application error processing RPC"

    @allure.title('Конвертация валют')
    @pytest.mark.parametrize("spend, spend_currency, desired_currency, expected_result", [
        (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
        (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
        (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
    ])
    def test_currency_conversion(
            self,
            grpc_client: NifflerCurrencyServiceClient,
            spend: float, spend_currency: CurrencyValues,
            desired_currency: CurrencyValues, expected_result: float):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=spend_currency,
                desiredCurrency=desired_currency,
                amount=spend
            )
        )
        assert response.calculatedAmount == expected_result, "Expected {expected_result}"
