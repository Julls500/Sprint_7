from helpers import Funcs, Courier, Order
import pytest
import allure
import logging
import sys

@allure.step('Генерация данных для регистрации курьера и удаление курьера после теста')
@pytest.fixture
def courier_payload():
    payload = Courier.generate_courier_payload()
    yield payload
    Courier.delete_courier_payload(payload)

@allure.step('Регистрация курьера в системе, возвращение "login" и "password" и удаление курьера после теста')
@pytest.fixture
def courier_login():
    c_data = Courier.register_new_courier_and_return_login_details()
    Funcs.remove_payload_param(c_data, 'firstName')
    yield c_data
    Courier.delete_courier_payload(c_data)

@allure.step('Создание курьера, получение ID и удаление курьера после теста')
@pytest.fixture
def courier_id():
    courier = Courier.create_courier_and_get_id()
    yield courier
    Courier.delete_courier_id(courier)

@allure.step('Создание заказа с проверкой наличия в системе, получение его track номера и отмена заказа после теста'
             ' (для случаев если он не был принят курьером и не был удален вместе со связанными заказами курьера).')
@pytest.fixture
def order_confirmed():
    order = Order.create_order_and_get_track()
    Order.check_order_is_in_the_system(order)
    yield order
    Order.cancel_order(order)

@allure.step('Инициализация логгера.')
@pytest.fixture(scope='session')
def logger():
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)
