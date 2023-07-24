from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from course_app.models import Course, Lesson, Payments, Subscription
from course_app.pagination import MaterialsPagination
from course_app.permissions import IsOwner, IsModerator
from course_app.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, PaymentIntentConfirmSerializer
from course_app.services import StripeService
from users.serializers import PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = MaterialsPagination
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAdminUser | IsModerator | IsOwner]


class LessonListView(generics.ListAPIView):
    pagination_class = MaterialsPagination
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'method_payment']
    ordering_fields = ['payment_date']
    permission_classes = [IsModerator | IsOwner]


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsModerator | IsOwner | IsAdminUser]


class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class PaymentIntentCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentIntentCreateSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user_id = request.user.id
            try:
                payment_intent = StripeService.create_payment_intent(course_id, user_id)
                payment = Payments.objects.get(payment_intent_id=payment_intent['id'])
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodCreateView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentMethodCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            payment_token = serializer.validated_data['payment_token']
            try:
                StripeService.connection(payment_intent_id, payment_token)
                payment = Payments.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentIntentConfirmSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            try:
                StripeService.confirm_payment_intent(payment_intent_id)
                payment = Payments.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
