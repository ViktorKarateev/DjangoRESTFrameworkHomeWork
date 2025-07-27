import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import retrieve_checkout_session
from .models import Payment


class CreateStripeSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Оплата курса',
                            },
                            'unit_amount': 1000,  # $10.00
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='https://example.com/success/',
                cancel_url='https://example.com/cancel/',
                customer_email=request.user.email,
            )

            Payment.objects.create(
                user=request.user,
                session_id=checkout_session.id,
                session_url=checkout_session.url,
                status=checkout_session.status
            )

            return Response({'session_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripeSessionStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = retrieve_checkout_session(session_id)

        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # 🟡 Обновляем статус в нашей модели Payment
        try:
            payment = Payment.objects.get(session_id=session_id, user=request.user)
            payment.status = result.get("status", payment.status)
            payment.save()
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)
