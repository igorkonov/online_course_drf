from django.urls import path
from rest_framework.routers import DefaultRouter

from course_app.apps import CourseAppConfig
from course_app.views import CourseViewSet, LessonListView, LessonCreateView, LessonDeleteView, LessonDetailView, \
    LessonUpdateView, PaymentListView, PaymentCreateView, PaymentDetailView, PaymentDeleteView, PaymentUpdateView, \
    SubscriptionCreateView, SubscriptionDeleteView, SubscriptionUpdateView

app_name = CourseAppConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/detail/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('payment/', PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/detail/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/delete/<int:pk>/', PaymentDeleteView.as_view(), name='payment_delete'),
    path('subscriptions/create/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('subscriptions/update/<int:pk>/', SubscriptionUpdateView.as_view(), name='subscription_update')

] + router.urls
