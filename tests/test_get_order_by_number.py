from helpers import Funcs, Order, Request
import config
import allure
import data

class TestGetOrderByNumber:

    @allure.title('200 OK успешное получение деталей заказа по его валидному номеру.')
    @allure.description('Создаем заказ и получаем его номер. Отправляем GET запрос на ручку /api/v1/orders/track?t=Track.'
                        ' Проверяем что ответ 200 OK, json содержит ожидаемый список полей и номер заказа в ответе совпадает с запрашиваемым.'
                        ' Затем заказ отменяется.')
    def test_get_order_by_number_valid_order_success_200(self):
        expected_track =  Order.create_order_and_get_track()
        expected_params_list = data.get_order_by_number_details.get('order').keys()
        path = f'{config.GET_ORDER_BY_TRACK}{expected_track}'
        response = Request.get(path)
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code}, {response.text}'
        actual_params_list = response.json().get('order').keys()
        assert actual_params_list == expected_params_list, f'Ожидалось: {expected_params_list}, получено {actual_params_list}'
        actual_order_track = response.json().get('order').get('track')
        assert actual_order_track == expected_track, f'Номер заказа в ответе не совпадает с запрашиваемым. Ожидалось {expected_track}, получено {actual_order_track}, {response.json()}'
        Order.cancel_order(expected_track)

    @allure.title('Ошибка 400 Bad Request при запросе на получение деталей заказа без номера заказа.')
    @allure.description('Отправляем GET запрос на ручку /api/v1/orders/track?t= без номера заказа. Проверяем что ответ 400 Bad Request'
                        ' и сообщение в теле ответа "Недостаточно данных для поиска"')
    def test_get_order_by_number_no_order_number_shows_error_400(self):
        response = Request.get(config.GET_ORDER_BY_TRACK)
        expected_message = "Недостаточно данных для поиска"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code}, {response.text}'
        actual_message = response.json()["message"]
        assert actual_message == expected_message, f'Ожидалось {expected_message}, получено {actual_message}, {response.json()}'

    @allure.title('Ошибка 404 Not Found при запросе на получение деталей заказа с несуществующим номером заказа.')
    @allure.description('Отправляем GET запрос на ручку /api/v1/orders/track?t= с несуществующим номером заказа.'
                        ' Проверяем что ответ 404 Not Found и сообщение в теле ответа "Заказ не найден"')
    def test_get_order_by_number_not_valid_order_number_shows_error_404(self):
        order_track = Funcs.generate_random_id()
        path = f'{config.GET_ORDER_BY_TRACK}{order_track}'
        response = Request.get(path)
        expected_message = "Заказ не найден"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code}, {response.text}'
        actual_message = response.json()["message"]
        assert actual_message == expected_message, f'Ожидалось {expected_message}, получено {actual_message}, {response.json()}'
