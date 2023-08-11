from rest_framework import status

from course_app.tests import SetupTestCase


class UserTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.test_data = {"email": "test@gmail.com", "password": "12345QWe", "phone": "111111", "city": "Testograd"}

    def test_user_create(self):
        response = self.client.post('/users/user/', self.test_data)

        self.assertEqual(response.json(), {'id': 9,
                                           "email": "test@gmail.com",
                                           "phone": "111111",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.get('/users/user/')

        self.assertEqual(response.json(), [{'id': 12,
                                            "email": "test@test.ru",
                                            "phone": "111111111",
                                            "city": "Testograd",
                                            "avatar": None},
                                           {'id': 13,
                                            "email": "test@gmail.com",
                                            "phone": "111111",
                                            "city": "Testograd",
                                            "avatar": None}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.get('/users/user/15/')

        self.assertEqual(response.json(), {"id": 15,
                                           "email": "test@gmail.com",
                                           "password": '',
                                           "phone": "111111",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.patch('/users/user/17/', {'phone': '555555'})

        self.assertEqual(response.json(), {"id": 17,
                                           "email": "test@gmail.com",
                                           "phone": "555555",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_destroy(self):
        self.client.post('/users/user/', self.test_data)
        response_1 = self.client.delete('/users/user/10/')
        response_2 = self.client.delete('/users/user/11/')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_401_UNAUTHORIZED)
