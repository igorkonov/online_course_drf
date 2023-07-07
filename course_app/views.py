from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from course_app.models import Course, Lesson, Payments
from course_app.serializers import CourseSerializer, LessonSerializer
from users.serializers import PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'method_payment']
    ordering_fields = ['payment_date']


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDeleteView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentUpdateView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
