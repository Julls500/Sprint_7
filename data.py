
#Headers
headers = {
    "Content-Type": "application/json"
}

# Данные для создания заказа
order_details = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2025-03-03",
    "comment": "Saske, come back to Konoha",
    "color": ["BLACK"]
    }

# Список заказов отдаваемый по ручке Получение списка заказов
orders_list = {
    "orders": [
        {
            "id": 5,
            "courierId": 'null',
            "firstName": "вфцфвц",
            "lastName": "вфцвфцв",
            "address": "вфцвфцвфц",
            "metroStation": "4",
            "phone": "1441412414",
            "rentTime": 4,
            "deliveryDate": "2020-06-08T21:00:00.000Z",
            "track": 189237,
            "color": [
                "BLACK",
                "GREY"
            ],
            "comment": "вфцвфцвфцв",
            "createdAt": "2020-06-21T13:23:09.404Z",
            "updatedAt": "2020-06-21T13:23:09.404Z",
            "status": 0
        }
    ],
    "pageInfo": {
        "page": 0,
        "total": 3,
        "limit": 2
    },
    "availableStations": [
        {
            "name": "Черкизовская",
            "number": "2",
            "color": "#D92B2C"
        },
        {
            "name": "Преображенская площадь",
            "number": "3",
            "color": "#D92B2C"
        },
        {
            "name": "Сокольники",
            "number": "4",
            "color": "#D92B2C"
        }
    ]
    }

#Детали заказа отдаваемые по ручке Получить заказ по его номеру (заказ не принят)

get_order_by_number_details = {
    "order": {
        "id": 2,
        "firstName": "Naruto",
        "lastName": "Uzumaki",
        "address": "Kanoha, 142 apt.",
        "metroStation": "1",
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06T00:00:00.000Z",
        "track": 521394,
        "status": 0,
        "color": ["BLACK"],
        "comment": "Saske, come back to Kanoha",
        "cancelled": False,
        "finished": False,
        "inDelivery": False,
        "createdAt": "2020-06-08T14:40:28.219Z",
        "updatedAt": "2020-06-08T14:40:28.219Z"
        }
    }
