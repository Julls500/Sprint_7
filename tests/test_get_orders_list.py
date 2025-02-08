from helpers import Funcs, Courier, Order, Request
import config
import allure

class TestGetOrdersList:

    @allure.title('200 OK успешное получение активных/завершенных заказов курьера.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID.'
                        ' Создаем заказ фикстурой order_confirmed, получаем его track. Фикстура также проверяет, что заказ создан и успешно находится в системе по track номеру.'
                        ' Курьер принимает заказ.'
                        ' Отправляем GET запрос на ручку /api/v1/orders?courierId=IDКурьера.'
                        ' Проверяем что ответ 200 OK, в списке вернулся 1 заказ и его track номер соответствует принятому заказу.'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_get_orders_list_orders_accepted_by_courier_success_200(self, courier_id, order_confirmed):
        Courier.accept_order(courier_id, order_confirmed)
        path = f'{config.COURIER_ORDERS}{courier_id}'
        response = Request.get(path)
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code}, {response.text}'
        assert len(response.json().get('orders')) == 1, f'Количество принятых курьером заказов не 1, {response.json().get('orders')}'
        actual_order_track = response.json()['orders'][0]["track"]
        assert actual_order_track == order_confirmed, f'Номер принятого заказа не совпадает с номером заказа в ответе. Ожидалось: {order_confirmed} , получено {actual_order_track}, {response.text}'

    @allure.title('200 OK успешное получение активных/завершенных заказов курьера на заданной станции метро.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID.'
                        ' Cоздаем заказ на станции метро 110 и на станции метро 89.'
                        ' Курьер принимает заказы.'
                        ' Отправляем GET запрос на ручку /api/v1/orders?courierId=IDКурьера&nearestStation=["110"]. Проверяем что ответ 200 OK,'
                        ' в списке вернулся 1 заказ на станции метро 110 и его track номер соответствует принятому заказу.'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_get_orders_list_orders_accepted_by_courier_set_station_success_200(self, courier_id):
        expected_station_1 = '110'
        expected_station_2 = '89'
        order_track_1 = Order.create_order_and_get_track_confirmed_line(expected_station_1)
        order_track_2 = Order.create_order_and_get_track_confirmed_line(expected_station_2)
        Courier.accept_order(courier_id, order_track_1)
        Courier.accept_order(courier_id, order_track_2)
        path = f'{config.COURIER_ORDERS}{courier_id}&nearestStation=["{expected_station_1}"]'
        response = Request.get(path)
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code}, {response.text}'
        assert len(response.json().get('orders')) == 1, f'Количество принятых курьером заказов на станции {expected_station_1} не 1, {response.json().get('orders')}'
        actual_station = response.json()['orders'][0]['metroStation']
        assert actual_station == expected_station_1, f'Станция метро в ответе не совпадает с ожидаемой. Ожидалось {expected_station_1}, получено {actual_station}'
        actual_order_track = response.json()['orders'][0]["track"]
        assert actual_order_track == order_track_1, f'Номер принятого заказа на станции {expected_station_1} не совпадает с номером заказа в ответе. Ожидалось: {order_track_1} , получено {actual_order_track}'

    @allure.title('Ошибка 404 Not Found при запросе на получение активных/завершенных заказов курьера с несуществующим ID курьера.')
    @allure.description('Отправляем GET запрос на ручку /api/v1/orders?courierId=IDКурьера с несуществующим ID. Проверяем что ответ 404 Not Found,'
                        ' и сообщение в теле ответа "Курьер с идентификатором {courierId} не найден"')
    def test_get_orders_list_orders_accepted_by_courier_not_valid_courier_id_shows_error_404(self):
        c_id = Funcs.generate_random_id()
        path = f'{config.COURIER_ORDERS}{c_id}'
        response = Request.get(path)
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code}, {response.text}'
        assert response.json()["message"] == f'Курьер с идентификатором {c_id} не найден'
