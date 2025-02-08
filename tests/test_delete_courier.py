from helpers import Funcs, Courier, Request
import config
import allure

class TestDeleteCourier:

    @allure.title('200 Успешное удаление существующего курьера из системы')
    @allure.description('Регистрируем курьера, получаем его ID, "password" и "login".'
                        ' Отправлям DELETE запрос на ручку DELETE/api/v1/courier/:id.'
                        ' Проверяем, что ответ 200 ОК, тело ответа {"ok":true}'
                        ' и при попытке залогиниться с теми же "password" и "login" возвращается ответ 404 Not Found')
    def test_delete_courier_valid_id_success_200(self):
        c_login = Courier.register_new_courier_and_return_login_details()
        c_id = Courier.courier_login(c_login)
        payload = {
            "id": c_id
        }
        path = f'{config.DELETE_COURIER_PATH}{c_id}'
        response = Request.delete(path, payload)
        expected_response_body = {"ok":True}
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.status_code} {response.text}'
        assert response.json() == expected_response_body, f'Ожидалось: {expected_response_body}, получено {response.json()}'
        account_deleted_check = Request.post(config.COURIER_LOGIN_PATH, c_login)
        assert account_deleted_check.status_code == 404, f'Курьер не удален: {response.status_code}, {response.text}.'

    @allure.title('Ошибка 400 Bad Request при запросе на удаление курьера без id в payload.')
    @allure.description('Создаем курьера фикстурой courier_id и получаем его ID.'
                        ' Отправлям DELETE запрос на ручку DELETE/api/v1/courier/:id без id курьера в payload.'
                        ' Проверяем, что ответ 400 Bad Request и сообщение в ответе "Недостаточно данных для удаления курьера".'
                        ' Курьер удаляется из системы фикстурой courier_id.')
    def test_delete_courier_no_id_in_payload_shows_error_400(self, courier_id):
        payload = {}
        path = f'{config.DELETE_COURIER_PATH}{courier_id}'
        response = Request.delete(path, payload)
        expected_message = "Недостаточно данных для удаления курьера"
        assert response.status_code == 400, f'Ожидалось: 400 Bad Request, получено {response.status_code} {response.text}'
        assert response.json()['message'] == expected_message, f'Ожидалось: {expected_message}, получено {response.json()}'

    @allure.title('Ошибка 404 Not Found при запросе на удаление курьера c несуществующим id.')
    @allure.description('Отправлям DELETE запрос на ручку DELETE/api/v1/courier/:id c несуществующим id.'
                        ' Проверяем, что ответ 404 Not Found и сообщение в ответе "Курьера с таким id нет"')
    def test_delete_courier_id_not_exists_shows_error_404(self):
        c_id = Funcs.generate_random_id()
        payload = {
            "id": str(c_id)
        }
        path = f'{config.DELETE_COURIER_PATH}{c_id}'
        response = Request.delete(path, payload)
        expected_message = "Курьера с таким id нет."
        assert response.status_code == 404, f'Ожидалось: 404 Not Found, получено {response.text}'
        assert response.json()['message'] == expected_message, f'Ожидалось: {expected_message}, получено {response.json()}'


