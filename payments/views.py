import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
            return Response({'session_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
