from rest_framework import serializers

from course_app.models import Course, Lesson, Subscription, Payments
from course_app.validators import VideoValidator, CourseIdValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        validators = [VideoValidator(field='video')]
        fields = (
            "name",
            "description",
            "preview",
            "video",
            "user",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        lessons = Lesson.objects.filter(course=instance).all()
        if lessons:
            return lessons.count()
        return 0

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            course = obj
            subscription = Subscription.objects.filter(course=course, user=user).first()
            if subscription:
                return subscription.status
        return False

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "price",
            "user",
            "subscription",
            "lessons_count",
            "lessons",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentIntentCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(validators=[CourseIdValidator(field='course_id')])


class PaymentMethodCreateSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=500)
    payment_token = serializers.CharField(max_length=255)

    def validate(self, value):
        payment_intent_id = value['payment_intent_id']
        payment = Payments.objects.get(payment_intent_id=payment_intent_id)
        if payment is None:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} не найден")
        if payment.confirmation:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} уже подтвержден")
        return value


class PaymentIntentConfirmSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=500)

    def validate(self, value):

        payment_intent_id = value['payment_intent_id']
        payment = Payments.objects.get(payment_intent_id=payment_intent_id)
        if payment is None:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} не найден")
        if payment.payment_method_id is None:
            raise serializers.ValidationError(f"К платежу с ID {payment_intent_id} не привязан метод платежа")
        if payment.confirmation:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} уже подтвержден")
        return value
