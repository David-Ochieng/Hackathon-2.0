import os
import requests
from requests.auth import HTTPBasicAuth
from config import Config
import stripe
from datetime import datetime

stripe.api_key = Config.STRIPE_SECRET_KEY

def create_stripe_checkout(session_success_url, session_cancel_url, customer_email=None):
    if not Config.STRIPE_PRICE_PRO_ID:
        raise Exception("STRIPE_PRICE_PRO_ID env var missing")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": Config.STRIPE_PRICE_PRO_ID, "quantity": 1}],
        success_url=session_success_url,
        cancel_url=session_cancel_url,
        customer_email=customer_email
    )
    return session

# M-Pesa: Get OAuth token (sandbox)
def mpesa_get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = HTTPBasicAuth(Config.MPESA_CONSUMER_KEY, Config.MPESA_CONSUMER_SECRET)
    r = requests.get(url, auth=auth)
    r.raise_for_status()
    return r.json().get("access_token")

# M-Pesa: STK Push (simplified)
def mpesa_stk_push(phone_number, amount, account_reference="MoodJournal", description="Subscription"):
    token = mpesa_get_token()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    password = (Config.MPESA_SHORTCODE + Config.MPESA_PASSKEY + timestamp).encode('utf-8')
    import base64
    password_b64 = base64.b64encode(password).decode('utf-8')

    payload = {
        "BusinessShortCode": Config.MPESA_SHORTCODE,
        "Password": password_b64,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(amount),
        "PartyA": phone_number,
        "PartyB": Config.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": Config.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": description
    }
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()
