from flask import request, jsonify
import stripe
from app._init_ import app

stripe.api_key = app.config['STRIPE_SECRET_KEY']

def create_customer(email):
    customer = stripe.Customer.create(email=email)
    return customer.id

def create_payment_method(customer_id, card_number, exp_month, exp_year, cvc):
    payment_method = stripe.PaymentMethod.create(
        type='card',
        card={
            'number': card_number,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvc': cvc
        },
        customer=customer_id
    )
    return payment_method.id

def create_subscription(customer_id, payment_method_id, plan_id):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{'plan': plan_id}],
        payment_method=payment_method_id
    )
    return subscription.id