from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from course_app.models import Course, Subscription, Lesson, Payments
from course_app.services import StripeService


@shared_task
def notify_course_updates(course_id):
    subscribers = Subscription.objects.filter(course__id=course_id, status=True)
    course = Course.objects.get(id=course_id)
    if course.last_update <= timezone.now() - timedelta(minutes=1):

        for subscriber in subscribers:
            send_mail(
                subject=f'Обновление курса {course.name}',
                message='В курсе появились новые материалы',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.user.email],
                fail_silently=False
            )
            print(f'Сообщение отправлено {subscriber.user.email}')
    else:
        print('Курс был обновлен менее 4 часов назад, уведомление не отправлено')

    course.last_update = timezone.now()
    course.save()


@shared_task
def notify_lesson_updates(lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course

    if course.last_update <= timezone.now() - timedelta(minutes=1):
        subscribers = Subscription.objects.filter(course=course, status=True)

        for subscriber in subscribers:
            send_mail(
                subject=f'Обновление урока {lesson.name}',
                message='В уроке появились новые материалы',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber.user.email],
                fail_silently=False
            )
            print(f'Сообщение отправлено {subscriber.user.email}')
        course.last_update = timezone.now()
        course.save()
    else:
        print('Курс был обновлен менее 1 часов назад, уведомление не отправлено')


@shared_task
def check_status_payment():
    payments = Payments.objects.filter(method_payment='transfer')
    for payment in payments:
        StripeService.confirm_payment_intent(payment_intent_id=payment.payment_intent_id)
