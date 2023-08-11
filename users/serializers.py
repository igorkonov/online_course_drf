from rest_framework import serializers

from course_app.models import Payments, Subscription
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        new_payment = Payments.objects.create(**validated_data)
        Subscription.objects.create(payment=new_payment)
        return new_payment

    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(source='payment_set', many=True, read_only=True)

    def create(self, validated_data):
        payment = validated_data.pop('payment_set', [])
        user = User.objects.create(**validated_data)

        for pay in payment:
            Payments.objects.create(user=user, **pay)

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'phone',
            'city',
            'avatar',
            'payment'
        )


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'city',
            'avatar'
        )
