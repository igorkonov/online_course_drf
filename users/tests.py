from rest_framework import status

from course_app.tests import SetupTestCase


class UserTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.test_data = {"email": "test@gmail.com", "password": "12345QWe", "phone": "111111", "city": "Testograd"}

    def test_user_create(self):
        response = self.client.post('/users/user/', self.test_data)

        self.assertEqual(response.json(), {'id': 15,
                                           "email": "test@gmail.com",
                                           "password": "12345QWe",
                                           "phone": "111111",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.get('/users/user/')

        self.assertEqual(response.json(), [{'id': 18,
                                            "email": "test@test.ru",
                                            "phone": "111111111",
                                            "city": "Testograd",
                                            "avatar": None},
                                           {'id': 19,
                                            "email": "test@gmail.com",
                                            "phone": "111111",
                                            "city": "Testograd",
                                            "avatar": None}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.get('/users/user/20/')

        self.assertEqual(response.json(), {"id": 20,
                                           "email": "test@test.ru",
                                           "password": self.user.password,
                                           "phone": "111111111",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        self.client.post('/users/user/', self.test_data)
        response = self.client.patch('/users/user/22/', {'phone': '555555'})

        self.assertEqual(response.json(), {"id": 22,
                                           "email": "test@test.ru",
                                           "password": self.user.password,
                                           "phone": "555555",
                                           "city": "Testograd",
                                           "avatar": None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_destroy(self):
        self.client.post('/users/user/', self.test_data)
        response_1 = self.client.delete('/users/user/16/')
        response_2 = self.client.delete('/users/user/17/')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_401_UNAUTHORIZED)
