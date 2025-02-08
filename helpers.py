import random
import string
import config
import allure
import data
import requests
import json

class Funcs:

    @staticmethod
    @allure.step('Генерация рандомной строки заданной длины')
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    @allure.step('Генерация рандомного ID')
    def generate_random_id():
        return random.randint(111111111, 999999999)

    @staticmethod
    @allure.step('Изменение одного из полей данных для соответствия тестовому сценарию.')
    def change_payload_param(param, key, value):
        param[key] = value
        return param

    @staticmethod
    @allure.step('Удаление одного из полей данных для соответствия тестовому сценарию.')
    def remove_payload_param(payload, param):
        del payload[param]
        return payload


class Courier:

    @staticmethod
    @allure.step('Генерация данных для регистрации курьера. Формат - словарь с "login", "password" и "firstName"')
    def generate_courier_payload():
        payload = {
            "login": Funcs.generate_random_string(10),
            "password": Funcs.generate_random_string(10),
            "firstName": Funcs.generate_random_string(10)
            }
        return payload

    @staticmethod
    @allure.step('Регистрация курьера, проверка успешного ответа и возвращение данных курьера для дальнейшего использования.')
    def register_new_courier_and_return_login_details():
        courier = Courier.generate_courier_payload()
        response = Request.post(config.CREATE_COURIER_PATH, courier)
        if response.status_code == 201:
            print(f'Курьер зарегистрирован, {courier}')
            return courier
        else:
            print(f'Курьер не зарегистрирован: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Логин курьера в системе, проверка успешного ответа и получение id курьера для дальнейшего использования.')
    def courier_login(courier):
        if 'firstName' in courier.keys():
            del courier['firstName']
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        if response.status_code == 200:
            courier_id = response.json().get('id')
            print(f'Курьер залогинился, получен id:{courier_id}')
            return courier_id
        else:
            print(f'Курьер не залогинился: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Регистрация курьера, логин и получение его ID')
    def create_courier_and_get_id():
        courier = Courier.register_new_courier_and_return_login_details()
        courier_id = Courier.courier_login(courier)
        return courier_id

    @staticmethod
    @allure.step('Удаление курьера из системы по id и проверка успешного ответа.')
    def delete_courier_id(courier_id):
        payload = {
            "id": str(courier_id)
            }
        path = config.DELETE_COURIER_PATH + str(courier_id)
        response = Request.delete(path, payload)
        if response.status_code != 200:
            print(f'Курьер не удален: {response.status_code}, {response.text}.')
        else:
            print('Курьер удален')

    @staticmethod
    @allure.step('Удаление курьера из системы по payload и проверка успешного ответа.')
    def delete_courier_payload(courier):
        c_id = Courier.courier_login(courier)
        Courier.delete_courier_id(c_id)

    @staticmethod
    @allure.step('Принятие заказа курьером')
    def accept_order(courier_id, order_track):
        path = f'{config.ACCEPT_ORDER_PATH}{order_track}?courierId={courier_id}'
        response = Request.put_no_payload(path)
        if response.status_code != 200:
            return print(f'Заказ не принят курьером: {response.status_code}, {response.text}.')
        else:
            print('Заказ принят курьером')


class Order:

    @staticmethod
    @allure.step('Создание заказа на заданной ветке метро, проверка наличия в системе и возвращение его номера')
    def create_order_and_get_track_confirmed_line(line):
        order = data.order_details.copy()
        Funcs.change_payload_param(order, "metroStation", line)
        response = Request.post(config.CREATE_ORDER_PATH, order)
        if response.status_code == 201:
            order_track = response.json().get('track')
            print(f'Заказ создан, track: {order_track}')
            Order.check_order_is_in_the_system(order_track)
            return order_track
        else:
            print(f'Заказ не создан: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Создание заказа с рандомным именем заказчика и получение его номера')
    def create_order_and_get_track():
        order = data.order_details.copy()
        name = Funcs.generate_random_string(6)
        surname = Funcs.generate_random_string(6)
        Funcs.change_payload_param(order, "firstName", name)
        Funcs.change_payload_param(order, "lastName", surname)
        response = Request.post(config.CREATE_ORDER_PATH, order)
        if response.status_code == 201:
            order_track = response.json().get('track')
            print(f'Заказ создан, track: {order_track}')
            return order_track
        else:
            print(f'Заказ не создан: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Проверка наличия заказа в системе, поиск по номеру.')
    def check_order_is_in_the_system(order_track):
        order_search = Request.get(f'{config.GET_ORDER_BY_TRACK}{order_track}')
        if order_search.status_code != 200 or order_search.json().get('order').get('track') != order_track:
            print(f'Заказ в системе не найден,{order_search.status_code}, {order_search.text}')
        else:
            print(f'Заказ {order_track} найден в системе')

    @staticmethod
    @allure.step('Получение списка полей из json Список заказов')
    def params_list(param):
        return param.get('orders')[0].keys()


class Request:

    @staticmethod
    @allure.step('POST request.')
    def post(path, payload):
        return requests.post(config.URL_SERVICE + path, headers=data.headers, data=json.dumps(payload))

    @staticmethod
    @allure.step('DELETE request.')
    def delete(path, payload):
        return requests.delete(config.URL_SERVICE + path, headers=data.headers, data=json.dumps(payload))

    @staticmethod
    @allure.step('PUT request.')
    def put(path, payload):
        return requests.put(config.URL_SERVICE + path, headers=data.headers, data=json.dumps(payload))

    @staticmethod
    @allure.step('PUT request без payload')
    def put_no_payload(path):
        return requests.put(config.URL_SERVICE + path)

    @staticmethod
    @allure.step('GET request.')
    def get(path):
        return requests.get(config.URL_SERVICE + path, headers=data.headers)
