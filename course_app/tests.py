from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from course_app.models import Course, Lesson
from users.models import User


class SetupTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', phone='111111111', city='Testograd', is_superuser=True, is_staff=True,
                         is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {"email": "test@test.ru", "password": "123QWE456RTY"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class CourseTestCase(SetupTestCase):
    def setUp(self):
        self.test_data = {'name': 'test', 'description': 'test'}
        self.test_response_data = {
            'name': 'test', 'preview': None, 'description': 'test', 'author': None,
            'subscription': False, 'lessons_count': 0, 'lessons': []
        }

    def test_course_create(self):
        response = self.client.post('/courses/course/', self.test_data)

        self.assertEqual(response.json(), self.test_response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_list(self):
        self.test_course_create()
        response = self.client.get('/courses/course/')

        self.assertEqual(response.json(), {"count": 1,
                                           "next": None,
                                           "previous": None,
                                           "results": [self.test_response_data]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_retrieve(self):
        self.test_course_create()
        response = self.client.get('/courses/course/4/')

        self.assertEqual(response.json(), self.test_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update(self):
        self.test_course_create()
        response = self.client.patch('/courses/course/5/', {'name': 'test!!!'})

        self.assertEqual(response.json(), {'name': 'test!!!',
                                           'preview': None,
                                           'description': 'test',
                                           'author': None,
                                           'subscription': False,
                                           'lessons_count': 0,
                                           'lessons': []})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_destroy(self):
        self.test_course_create()
        response = self.client.delete('/courses/course/2/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.test_data = {'name': 'test', 'description': 'test',
                          'video': 'https://www.youtube.com/watch?v=747w5Zjm-C4&ab_channel=AlexTerrible'}
        self.test_response_data = {'name': 'test', 'description': 'test', 'preview': None,
                                   'video': 'https://www.youtube.com/watch?v=747w5Zjm-C4&ab_channel=AlexTerrible',
                                   'author': self.user.id}

    def test_lesson_create(self):
        response = self.client.post('/courses/lesson/create/', self.test_data)

        self.assertEqual(response.json(), self.test_response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lessons_list(self):
        self.test_lesson_create()
        response = self.client.get('/courses/lesson/')

        self.assertEqual(response.json(), {"count": 1,
                                           "next": None,
                                           "previous": None,
                                           "results": [self.test_response_data]
                                           })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessons_retrieve(self):
        self.test_lesson_create()
        response = self.client.get('/courses/lesson/detail/4/')

        self.assertEqual(response.json(), self.test_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessons_update(self):
        self.test_lesson_create()
        response = self.client.patch('/courses/lesson/update/5/', {'name': 'test!!!'})

        self.assertEqual(response.json(), {'name': 'test!!!',
                                           'description': 'test',
                                           'preview': None,
                                           'video': 'https://www.youtube.com/watch?v=747w5Zjm-C4&ab_channel=AlexTerrible',
                                           'author': self.user.id
                                           })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessons_destroy(self):
        self.test_lesson_create()
        response = self.client.delete('/courses/lesson/delete/2/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribeTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(name='test', description='test')

    def test_subscription_create(self):
        response = self.client.post('/courses/subscriptions/create/',
                                    {'course': self.course.id, 'user': self.user.id, 'status': True})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_update(self):
        self.test_subscription_create()
        response = self.client.patch('/courses/subscriptions/update/3/', {'status': False})

        self.assertEqual(response.json(),
                         {'id': 3, 'course': self.course.id, 'user': self.user.id, 'status': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_delete(self):
        self.test_subscription_create()
        response = self.client.delete('/courses/subscriptions/delete/2/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PaymentsTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.course = Course.objects.create(name='test', description='test')
        self.lesson = Lesson.objects.create(name='test', description='test')

        self.test_data_course = {"payment_amount": 45000, "method_payment": "cash", "user": self.user.id,
                                 "paid_course": self.course.id}
        self.test_data_lesson = {"payment_amount": 5000, "method_payment": "transfer", "user": self.user.id,
                                 "paid_lesson": self.lesson.id}

    def test_payment_create(self):
        response_1 = self.client.post('/courses/payment/create/', self.test_data_course)
        response_2 = self.client.post('/courses/payment/create/', self.test_data_lesson)

        expected_course_payment = {"id": 1,
                                   "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                   "payment_amount": 45000,
                                   "method_payment": "cash",
                                   "user": self.user.id,
                                   "paid_course": self.course.id,
                                   "paid_lesson": None
                                   }
        expected_lesson_payment = {"id": 2,
                                   "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                   "payment_amount": 5000,
                                   "method_payment": "transfer",
                                   "user": self.user.id,
                                   "paid_course": None,
                                   "paid_lesson": self.lesson.id
                                   }
        self.assertEqual(response_1.json(), expected_course_payment)
        self.assertEqual(response_2.json(), expected_lesson_payment)

        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

    def test_payment_list(self):
        self.client.post('/courses/payment/create/', self.test_data_course)
        self.client.post('/courses/payment/create/', self.test_data_lesson)
        response = self.client.get('/courses/payment/')

        self.assertEqual(response.json(), [{"id": 5,
                                            "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                            "payment_amount": 45000,
                                            "method_payment": "cash",
                                            "user": self.user.id,
                                            "paid_course": self.course.id,
                                            "paid_lesson": None
                                            },
                                           {"id": 6,
                                            "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                            "payment_amount": 5000,
                                            "method_payment": "transfer",
                                            "user": self.user.id,
                                            "paid_course": None,
                                            "paid_lesson": self.lesson.id
                                            }])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_retrieve(self):
        self.client.post('/courses/payment/create/', self.test_data_course)
        self.client.post('/courses/payment/create/', self.test_data_lesson)
        response_1 = self.client.get('/courses/payment/detail/7/')
        response_2 = self.client.get('/courses/payment/detail/8/')

        self.assertEqual(response_1.json(), {"id": 7,
                                             "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                             "payment_amount": 45000,
                                             "method_payment": "cash",
                                             "user": self.user.id,
                                             "paid_course": self.course.id,
                                             "paid_lesson": None
                                             })
        self.assertEqual(response_2.json(), {"id": 8,
                                             "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                             "payment_amount": 5000,
                                             "method_payment": "transfer",
                                             "user": self.user.id,
                                             "paid_course": None,
                                             "paid_lesson": self.lesson.id
                                             })

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_payment_update(self):
        self.client.post('/courses/payment/create/', self.test_data_course)
        self.client.post('/courses/payment/create/', self.test_data_lesson)
        response_1 = self.client.patch('/courses/payment/update/9/',
                                       {"method_payment": "transfer", "paid_lesson": self.lesson.id})
        response_2 = self.client.patch('/courses/payment/update/10/', {"method_payment": "cash"})

        self.assertEqual(response_1.json(), {"id": 9,
                                             "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                             "payment_amount": 45000,
                                             "method_payment": "transfer",
                                             "user": self.user.id,
                                             "paid_course": self.course.id,
                                             "paid_lesson": self.lesson.id
                                             })
        self.assertEqual(response_2.json(), {"id": 10,
                                             "payment_date": datetime.now().strftime('%Y-%m-%d'),
                                             "payment_amount": 5000,
                                             "method_payment": "cash",
                                             "user": self.user.id,
                                             "paid_course": None,
                                             "paid_lesson": self.lesson.id
                                             })
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_payment_destroy(self):
        self.client.post('/courses/payment/create/', self.test_data_course)
        self.client.post('/courses/payment/create/', self.test_data_lesson)
        response_1 = self.client.delete('/courses/payment/delete/3/')
        response_2 = self.client.delete('/courses/payment/delete/4/')

        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_204_NO_CONTENT)
