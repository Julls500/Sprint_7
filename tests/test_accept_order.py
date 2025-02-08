from helpers import Funcs, Order, Request, Courier
import config
import pytest
import allure

@pytest.mark.usefixtures('class_courier')
class TestAcceptOrder:

    @allure.title('200 OK при запросе на принятие 1 заказа курьером с валидным заказом и курьером.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID,'
                        ' создаем заказ фикстурой order_confirmed, Фикстура также проверяет, что заказ создан и успешно находится в системе по track номеру.'
                        ' Отправлям PUT запрос на ручку /api/v1/orders/accept/OrderID?courierId=CourierID.'
                        ' Проверяем, что ответ 200 ОК и тело ответа {"ok":true}.'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_accept_order_valid_order_and_courier_success_200(self, courier_id, order_confirmed):
        path = f'{config.ACCEPT_ORDER_PATH}{order_confirmed}?courierId={courier_id}'
        response = Request.put_no_payload(path)
        expected_response_body = {"ok": True}
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code} {response.text}'
        assert response.json() == expected_response_body, f'Ожидалось: {expected_response_body}, получено {response.json()}'

    @allure.title('Ошибка 400 Bad Request при запросе на принятие заказа без ID курьера.')
    @allure.description('Создаем заказ фикстурой order_confirmed. Отправляем PUT запрос на ручку /api/v1/orders/accept/OrderID?courierId=CourierID без ID курьера.'
                        ' Проверяем, что код ответа 400 Bad Request и текст ответа "Недостаточно данных для поиска"')
    def test_accept_order_valid_order_no_courier_id_shows_error_400(self, order_confirmed):
        path = f'{config.ACCEPT_ORDER_PATH}{order_confirmed}?courierId='
        response = Request.put_no_payload(path)
        expected_response_message = "Недостаточно данных для поиска"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено {response.json()}'

    @allure.title('Ошибка 400 Bad Request при запросе на принятие заказа без номера заказа.')
    @allure.description('Создаем курьера фикстурой courier_id. Отправляется PUT запрос на ручку /api/v1/orders/accept/OrderID?courierId=CourierID без номера заказа. '
                        ' Проверяем, что код ответа 400 Bad Request и текст ответа "Недостаточно данных для поиска"'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_accept_order_valid_courier_no_order_id_shows_error_400(self, courier_id):
        path = f'{config.ACCEPT_ORDER_PATH}?courierId={courier_id}'
        response = Request.put_no_payload(path)
        expected_response_message = "Недостаточно данных для поиска"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено {response.json()}'

    @allure.title('Ошибка 404 Not Found при запросе на принятие заказа c несуществующим ID курьера.')
    @allure.description('Создаем заказ фикстурой order_confirmed. Отправляется PUT запрос на ручку /api/v1/orders/accept/OrderID?courierId=CourierID c несуществующим ID курьера.'
                        ' Проверяем, что код ответа 404 Not Found и текст ответа "Курьера с таким id не существует"')
    def test_accept_order_valid_order_id_not_valid_courier_id_shows_error_404(self, order_confirmed):
        c_id = Funcs.generate_random_id()
        path = f'{config.ACCEPT_ORDER_PATH}{order_confirmed}?courierId={c_id}'
        response = Request.put_no_payload(path)
        expected_response_message = "Курьера с таким id не существует"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено {response.json()}'

    @allure.title('Ошибка 404 Not Found при запросе на принятие заказа c несуществующим ID заказа.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID. Отправляется PUT запрос на ручку /api/v1/orders/accept/orderID?courierId=CourierID c несуществующим ID заказа.'
                        ' Проверяем, что код ответа 404 Not Found и текст ответа "Заказа с таким id не существует"'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_accept_order_valid_courier_id_not_valid_order_id_shows_error_404(self, courier_id):
        order_track = Funcs.generate_random_id()
        path = f'{config.ACCEPT_ORDER_PATH}{order_track}?courierId={courier_id}'
        response = Request.put_no_payload(path)
        expected_response_message = "Заказа с таким id не существует"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено {response.json()}'

    @allure.title('409 Conflict при повторном принятии заказа c курьером.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID.'
                        ' Cоздаем заказ фикстурой order_confirmed. Фикстура также проверяет, что заказ создан и успешно находится в системе по track номеру.'
                        ' Отправляется PUT запрос на ручку /api/v1/orders/accept/orderID?courierId=CourierID.'
                        ' Отправляется повторный PUT запрос на ручку /api/v1/orders/accept/orderID?courierId=CourierID. Проверяем, что код ответа 409 Conflict'
                        ' и текст ответа "Этот заказ уже в работе". Курьер удаляется из системы фикстурой courier_id.')
    def test_accept_order_accept_same_order_twice_shows_error_409(self, courier_id, order_confirmed):
        path = f'{config.ACCEPT_ORDER_PATH}{order_confirmed}?courierId={courier_id}'
        Courier.accept_order(courier_id, order_confirmed)
        response = Request.put_no_payload(path)
        expected_response_message = "Этот заказ уже в работе"
        assert response.status_code == 409, f'Ожидалось: 409 Conflict, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено {response.json()}'

    @allure.title('200 OK при запросе на принятие 5 валидных заказов подряд 1 курьером.')
    @allure.description('Создаем курьера фикстурой class_courier для всего класса и получаем его ID. В рамках параметрического теста создается заказ'
                        ' на заданной станции метро. Также проверяется, что заказ создан и успешно находится в системе по track номеру.'
                        ' Отправляется PUT запрос на ручку /api/v1/orders/accept/OrderID?courierId=CourierID для принятия заказа курьером class_courier.'
                        ' Проверяем, что каждый заказ принят, ответ 200 ОК и тело ответа {"ok":true}.')
    @pytest.mark.parametrize('station', ['107', '108', '109', '110', '111'])
    def test_accept_order_10_orders_accepted_by_courier_success_200(self, class_courier, station):
        order_track = Order.create_order_and_get_track_confirmed_line(station)
        path = f'{config.ACCEPT_ORDER_PATH}{order_track}?courierId={class_courier}'
        response = Request.put_no_payload(path)
        expected_response_body = {"ok": True}
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        assert response.json() == expected_response_body, f'Ожидалось: {expected_response_body}, получено {response.json()}'
