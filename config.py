#Сервис Яндекс Самокат
URL_SERVICE = 'http://qa-scooter.praktikum-services.ru'

#Ручка Создание курьера
CREATE_COURIER_PATH = '/api/v1/courier'

#Ручка Логин курьера в системе
COURIER_LOGIN_PATH = '/api/v1/courier/login'

#Ручка Удаление курьера '/api/v1/courier/:id'
DELETE_COURIER_PATH = '/api/v1/courier/'

#Ручка Создание заказа
CREATE_ORDER_PATH = '/api/v1/orders'

#Ручка Отменить заказ
CANCEL_ORDER_PATH = '/api/v1/orders/cancel'

#Ручка 10 заказов доступных для взятия курьером
GET_10_ORDERS_LIST = '/api/v1/orders/?limit=10&page=0'

#Ручка 10 заказов доступных для взятия курьером возле метро Калужская /api/v1/orders/?limit=10&page=0&nearestStation=["110"]
GET_10_ORDERS_NEAR_STATION_LIST = f'/api/v1/orders/?limit=10&page=0&nearestStation='

#Ручка Все активные/завершенные заказы курьера /api/v1/orders/?courierId=1
COURIER_ORDERS = '/api/v1/orders/?courierId='

#Ручка Все активные/завершенные заказы курьера c id = 1 на станции Калужская
COURIER_ORDERS_NEAR_STATION = '/api/v1/orders/?courierId=1&nearestStation=["110"]'

#Ручка Принять заказ api/v1/orders/accept/1?courierId=213
ACCEPT_ORDER_PATH = '/api/v1/orders/accept/'

#Ручка Получить заказ по его номеру /api/v1/orders/track
GET_ORDER_BY_TRACK = '/api/v1/orders/track?t='