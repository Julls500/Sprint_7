import config
import allure
from helpers import Funcs, Courier, Request

class TestCourierLogin:

    @allure.title('200 OK успешная авторизация курьера в системе с валидными "login" и "password".')
    @allure.description('Регистрируем курьера в системе и сохраняем "login" и "password" фикстурой courier_login.'
                        ' Отправлям POST запрос на ручку /api/v1/courier/login с данными курьера.'
                        ' Проверяем, что ответ 200 ОК, тело ответа содержит json c id курьера и id - число.'
                        ' Курьер удаляется из системы фикстурой courier_login.')
    def test_courier_login_valid_params_success_200(self, courier_login):
        response = Request.post(config.COURIER_LOGIN_PATH, courier_login)
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code} {response.text}'
        assert 'id' in response.json().keys() and len(str(response.json().get('id'))) != 0, f'Id не получен: {response.json()}'
        assert isinstance(response.json().get('id'), int), f'Id не число: {response.json()}'

    @allure.title('Ошибка 400 Bad Request при авторизации курьера в системе без обязательного параметра "login" и с валидным "password".')
    @allure.description('Регистрируем курьера в системе и сохраняем "login" и "password" фикстурой courier_login.'
                        ' Удаляем "login" и отправлям POST запрос на ручку /api/v1/courier/login.'
                        ' Проверяем, что ответ 400 Bad Request и сообщение об ошибке "Недостаточно данных для входа".'
                        ' Курьер удаляется из системы фикстурой courier_login.')
    def test_courier_login_no_login_valid_password_shows_error_400(self, courier_login):
        courier = courier_login.copy()
        Funcs.change_payload_param(courier,'login', "")
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        expected_response_message = "Недостаточно данных для входа"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено: {response.text}'

    @allure.title('Ошибка 400 Bad Request при авторизации курьера в системе без обязательного параметра "password" и с валидным "login".')
    @allure.description('Регистрируем курьера в системе и сохраняем "login" и "password" фикстурой courier_login.'
                        ' Удаляем "password" и отправляем POST запрос на ручку /api/v1/courier/login.'
                        ' Проверяем, что ответ 400 Bad Request и сообщение об ошибке "Недостаточно данных для входа".'
                        ' Курьер удаляется из системы фикстурой courier_login.')
    def test_courier_login_no_password_valid_login_shows_error_400(self, courier_login):
        courier = courier_login.copy()
        Funcs.change_payload_param(courier, 'password', "")
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        expected_response_message = "Недостаточно данных для входа"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено: {response.text}'

    @allure.title('Ошибка 404 Not Found при авторизации курьера в системе c неверным "login" и валидным "password".')
    @allure.description('Регистрируем курьера в системе и сохраняем "login" и "password" фикстурой courier_login.'
                        ' Изменяем "login" и отправлям POST запрос на ручку /api/v1/courier/login.'
                        ' Проверяем, что ответ 409 Not Found и сообщение об ошибке "Учетная запись не найдена".'
                        ' Курьер удаляется из системы фикстурой courier_login.')
    def test_courier_login_wrong_login_valid_password_shows_error_404(self, courier_login):
        courier = courier_login.copy()
        new_login = Funcs.generate_random_string(10)
        Funcs.change_payload_param(courier, 'login', new_login)
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        expected_response_message = "Учетная запись не найдена"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено: {response.text}'

    @allure.title('Ошибка 404 Not Found при авторизации курьера в системе c неверным "password" и валидным "login".')
    @allure.description('Регистрируем курьера в системе и сохраняем "login" и "password" фикстурой courier_login.'
                        ' Изменяем "password" и отправлям POST запрос на ручку /api/v1/courier/login.'
                        ' Проверяем, что ответ 409 Not Found и сообщение об ошибке "Учетная запись не найдена".'
                        ' Курьер удаляется из системы фикстурой courier_login.')
    def test_courier_login_wrong_password_valid_login_shows_error_404(self, courier_login):
        courier = courier_login.copy()
        new_password = Funcs.generate_random_string(10)
        Funcs.change_payload_param(courier, 'password', new_password)
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        expected_response_message = "Учетная запись не найдена"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено: {response.text}'

    @allure.title('Ошибка 404 Not Found при авторизации курьера в системе c несуществующими "password" и "login".')
    @allure.description('Генерируем данные курьера. На основе данных курьера формируем и отправлям POST запрос на ручку /api/v1/courier/login.'
                        ' Проверяем, что ответ 409 Not Found и сообщение об ошибке "Учетная запись не найдена".')
    def test_courier_login_wrong_password_and_login_shows_error_404(self):
        courier = Courier.generate_courier_payload()
        Funcs.remove_payload_param(courier, 'firstName')
        response = Request.post(config.COURIER_LOGIN_PATH, courier)
        expected_response_message = "Учетная запись не найдена"
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.status_code} {response.text}'
        assert response.json().get('message') == expected_response_message, f'Ожидалось: {expected_response_message}, получено: {response.text}'