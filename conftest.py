import config
from helpers import Funcs, Courier, Order, Request
import pytest
import allure
import data
import requests

@allure.step('Генерация данных для регистрации курьера и удаление курьера после теста')
@pytest.fixture
def courier_payload():
    payload = Courier.generate_courier_payload()
    yield payload
    Courier.delete_courier_payload(payload)

@allure.step('Генерация данных для регистрации курьера')
@pytest.fixture
def courier_data():
    return Courier.generate_courier_payload()

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

@allure.step('Создание заказа с проверкой наличия в системе и получение его track номера')
@pytest.fixture
def order_confirmed():
    order_track = Order.create_order_and_get_track()
    Order.check_order_is_in_the_system(order_track)
    return order_track

@allure.step('Создание курьера для параметрического теста test_accept_order_10_orders_accepted_by_courier_success_200 и удаление его после теста')
@pytest.fixture(scope='class')
def class_courier():
    class_courier = Courier.create_courier_and_get_id()
    yield class_courier
    Courier.delete_courier_id(class_courier)
