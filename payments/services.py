import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def retrieve_checkout_session(session_id: str) -> dict:
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "id": session.id,
            "status": session.status,
            "payment_status": session.payment_status,
            "customer_email": session.customer_email,
            "amount_total": session.amount_total
        }
    except stripe.error.InvalidRequestError as e:
        return {"error": str(e)}
