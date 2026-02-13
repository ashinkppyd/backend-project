import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency="inr",
        automatic_payment_methods={"enabled": True},
    )
