from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase

from course_app.models import Course, Subscription, Payments
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
            'name': 'test', 'preview': None, 'description': 'test', 'price': 5000, 'user': None,
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
                                           'price': 5000,
                                           'user': None,
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
                                   'user': self.user.id}

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
                                           'user': self.user.id
                                           })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessons_destroy(self):
        self.test_lesson_create()
        response = self.client.delete('/courses/lesson/delete/2/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribeTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.course = Course.objects.create(
            name='Test course',
            description='Test description',
            price=100
        )

    def test_subscription_create(self):
        payment = Payments.objects.create(payment_amount=100, user=self.user)
        data = {
            'course': self.course.id,
            'user': self.user.id,
            'payment': payment.id
        }

        response = self.client.post('/courses/subscriptions/create/', data)
        self.assertEqual(response.status_code, 201)

        subscription = Subscription.objects.get(id=response.data['id'])
        self.assertEqual(subscription.course, self.course)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.payment, payment)
        self.assertFalse(subscription.status)

    def test_subscription_delete(self):
        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
            payment=Payments.objects.create(user=self.user, payment_amount=100)
        )

        url = f'/courses/subscriptions/delete/{subscription.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ObjectDoesNotExist):
            Subscription.objects.get(id=subscription.id)
