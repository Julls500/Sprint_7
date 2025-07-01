from helpers import Funcs, Request, Order
import config
import pytest
import allure
import data

class TestCreateOrderColorSelection:

    @allure.title('201 Created успешное создание заказа с любым сочетанием цветов "BLACK" и "GREY".')
    @allure.description('Параметрический тест, проверяющий создание заказа с различным сочетанием цветов "BLACK" и "GREY", и без выбора цвета.'
                        'Формируется payload заказа и отправляется POST запрос на ручку /api/v1/orders.'
                        'Проверяем, что ответ 201 Created, тело ответа содержит json c track номером заказа и track - число. Затем заказ отменяется.')
    @pytest.mark.parametrize('color', [[], ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_create_order_any_color_selection_success_201(self, color):
        order_copy = data.order_details.copy()
        Funcs.change_payload_param(order_copy, "color", color)
        response = Request.post(config.CREATE_ORDER_PATH, order_copy)
        order_track = response.json().get('track')
        assert response.status_code == 201, f'Ожидалось: 201 Created, получено {response.status_code} {response.text}'
        assert 'track' in response.json().keys() and len(str(order_track)) != 0, f'Track не получен: {response.json()}'
        assert isinstance(order_track, int), f'Track не число: {response.json()}'
        Order.cancel_order(order_track)