import config
from helpers import Funcs, Courier, Request
import allure
import pytest

class TestCreateCourier:

    @allure.title('201 Created успешная регистрация курьера в системе с валидными "login", "password" и "firstName"')
    @allure.description('Генерируем данные курьера фикстурой courier_payload,'
                        ' отправлям POST запрос на ручку /api/v1/courier,'
                        ' проверяем, что ответ 201 Created и тело ответа {"ok":true}.'
                        ' Cозданный курьер удаляется из системы фикстурой courier_payload.')
    def test_create_courier_valid_params_success_201(self, courier_payload):
        response = Request.post(config.CREATE_COURIER_PATH, courier_payload)
        expected_response_body = {"ok":True}
        assert response.status_code == 201, f'Ожидалось: 201 Created, получено {response.status_code} {response.text}'
        assert response.json() == expected_response_body, f'Ожидалось: {expected_response_body}, получено {response.json()}'

    @allure.title('201 Created успешная регистрация курьера без необязательного поля "firstName" и с валидными "login" и "password".')
    @allure.description('Генерируем данные курьера фикстурой courier_payload,'
                        ' убираем "firstName", отправлям POST запрос на ручку /api/v1/courier,'
                        ' проверяем, что ответ 201 Created и тело ответа {"ok":true}.'
                        ' Cозданный курьер удаляется из системы фикстурой courier_payload.')
    def test_create_courier_no_firstname_success_201(self, courier_payload):
        Funcs.change_payload_param(courier_payload, 'firstName', "")
        response = Request.post(config.CREATE_COURIER_PATH, courier_payload)
        expected_response_body = {"ok":True}
        assert response.status_code == 201, f'Ожидалось: 201 Created, получено {response.status_code} {response.text}'
        assert response.json() == expected_response_body, f'Ожидалось: {expected_response_body}, получено {response.json()}'

    @allure.title('Ошибка 400 Bad Request при регистрации курьера без обязательного поля "password" или "login" и с валидным "firstName".')
    @allure.description('Параметрический тест, проверяющий появление ошибки при регистрации курьера без обязательного поля "password" или "login".'
                        'Генерируем данные курьера, изменяем на "" один из обязательных парметров и отправлям POST запрос на ручку /api/v1/courier,'
                        ' проверяем, что ответ 400 Bad Request и тело ответа {"message": "Недостаточно данных для создания учетной записи"}.')
    @pytest.mark.parametrize('key_to_change', ['login', 'password'])
    def test_create_courier_without_required_param_shows_error_400(self, key_to_change):
        courier_data = Courier.generate_courier_payload()
        Funcs.change_payload_param(courier_data, key_to_change, "")
        response = Request.post(config.CREATE_COURIER_PATH, courier_data)
        expected_response_text = "Недостаточно данных для создания учетной записи"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json()["message"] == expected_response_text, f'Ожидалось: {expected_response_text}, получено {response.json()}'

    @allure.title('Ошибка 409 Сonflict при повторной регистрации курьера с валидными "login", "password" и "firstName".')
    @allure.description('Генерируем данные курьера фикстурой courier_payload, регистрируем его в системе.'
                        'Отправлям повторный POST запрос на ручку /api/v1/courier для регистрации с теми же данными.'
                        ' Проверяем, что ответ 409 Сonflict и тело ответа {"message": "Этот логин уже используется"}.'
                        ' Созданный курьер удаляется из системы фикстурой courier_payload.')
    def test_create_courier_same_login_details_shows_error_409(self, courier_payload):
        Request.post(config.CREATE_COURIER_PATH, courier_payload)
        response = Request.post(config.CREATE_COURIER_PATH, courier_payload)
        expected_response_text = "Этот логин уже используется. Попробуйте другой."
        assert response.status_code == 409, f'Ожидалось: 409 Сonflict, получено {response.status_code} {response.text}'
        assert response.json()["message"] == expected_response_text, f'Ожидалось: {expected_response_text}, получено {response.json()}'

    @allure.title('Ошибка 409 Сonflict при регистрации курьера с уже существующим "login" и уникальными "password" и "firstName".')
    @allure.description('Генерируем данные курьера фикстурой courier_payload, регистрируем его в системе.'
                        ' Создаем данные для второго курьра с таким же "login" и уникальными "password" и "firstName".'
                        ' Отправлям POST запрос на ручку /api/v1/courier для регистрации.'
                        ' Проверяем, что ответ 409 Сonflict и тело ответа {"message": "Этот логин уже используется"}.'
                        ' Созданный курьер удаляется из системы фикстурой courier_payload.')
    def test_create_courier_same_login_new_firstname_and_password_shows_error_409(self, courier_payload):
        Request.post(config.CREATE_COURIER_PATH, courier_payload)
        new_courier_payload = Courier.generate_courier_payload()
        Funcs.change_payload_param(new_courier_payload, 'login', courier_payload.get('login'))
        response = Request.post(config.CREATE_COURIER_PATH, new_courier_payload)
        expected_response_text = "Этот логин уже используется. Попробуйте другой."
        assert response.status_code == 409, f'Ожидалось: 409 Сonflict, получено {response.status_code} {response.text}'
        assert response.json()["message"] == expected_response_text, f'Ожидалось: {expected_response_text}, получено {response.json()}'
