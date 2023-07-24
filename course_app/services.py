import requests

from config import settings
from course_app.models import Course, Payments, Subscription
from users.models import User


class StripeService:
    api_key = settings.STRIPE_SECRET_KEY
    headers = {'Authorization': f'Bearer {api_key}'}
    base_url = 'https://api.stripe.com/v1'

    @classmethod
    def create_payment_intent(cls, course_id, user_id):
        course = Course.objects.get(id=course_id)
        amount = course.price
        user = User.objects.get(id=user_id)

        data = [
            ('amount', amount * 100),
            ('currency', 'rub'),
            ('metadata[course_id]', course.id),
            ('metadata[user_id]', user.id)
        ]
        response = requests.post(f'{cls.base_url}/payment_intents', headers=cls.headers, data=data)

        if response.status_code != 200:
            raise Exception(f'Ошибка намерения платежа: {response.status_code}')

        payment_intent = response.json()

        payment = Payments.objects.create(
            user=user,
            paid_course=course,
            payment_amount=course.price,
            payment_intent_id=payment_intent['id'],
            status=payment_intent['status']
        )
        Subscription.objects.create(
            course=course,
            user=user,
            payment=payment,
            status=False
        )

        return payment_intent

    @classmethod
    def create_payment_method(cls, payment_token):

        data = {
            'type': 'card',
            'card[token]': payment_token,
        }

        response = requests.post(f'{cls.base_url}/payment_methods', headers=cls.headers, data=data)
        payment_method = response.json()

        if response.status_code != 200:
            raise Exception(f'Ошибка метода платежа: {response.status_code}')
        return payment_method

    @classmethod
    def connection(cls, payment_intent_id, payment_token):
        payment_method = cls.create_payment_method(payment_token)
        data = {'payment_method': payment_method['id']}
        response = requests.post(f'{cls.base_url}/payment_intents/{payment_intent_id}', headers=cls.headers, data=data)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f'Ошибка соединения метода и намерения платежа {response.status_code}')

        payment = Payments.objects.get(payment_intent_id=payment_intent_id)
        payment.payment_method_id = payment_method['id']
        payment.status = response_data['status']
        payment.save()

        return payment_method

    @classmethod
    def confirm_payment_intent(cls, payment_intent_id):
        payment = Payments.objects.get(payment_intent_id=payment_intent_id)
        url = f'{cls.base_url}/payment_intents/{payment_intent_id}/confirm'
        if payment.payment_method_id:
            data = {'payment_method': payment.payment_method_id}
            response = requests.post(url, headers=cls.headers, data=data)
        else:
            response = requests.post(url, headers=cls.headers)

        response_data = response.json()
        if response.status_code != 200:
            raise Exception(f'Ошибка подтверждения платежа: {response.status_code}')

        payment.status = response_data['status']
        payment.save()

        if payment.status == 'succeeded':
            # Оплата прошла успешно, активируем подписку
            subscription = Subscription.objects.get(payment=payment)
            subscription.status = True
            subscription.save()

        return response_data
