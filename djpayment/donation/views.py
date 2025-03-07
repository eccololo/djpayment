from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid
import time
import stripe

from .models import Donation


def my_donation(request):

    # PAYPAL FUNCTIONALITY
    # get the current host of requested website
    host = request.get_host()

    # get item from Donation model
    donation = Donation.objects.get(id=1)

    # paypal dict with PayPal API keys.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': donation.amount, # in set currency
        'item_name': donation.title,
        'no_shipping': '2', # User will be able to change his shipping address.
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': "http://{}{}".format(host, reverse("paypal-ipn")), # sending notification via PayPal IPN
        'return_url': "http://{}{}".format(host, reverse("payment-success")),
        'cancel_return': "http://{}{}".format(host, reverse("payment-failed")),
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    
    # STRIPE FUNCTIONALITY
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': 'price_1R01juRsmckp34rTZcVL3a0s',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment-success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('payment-failed'))
    )


    context = {
        'paypal_form': paypal_form
    }

    return render(request, template_name="donation/my-donation.html", context=context)


def payment_success(request):

    # time.sleep(10) # for ngrok

    return render(request, template_name="donation/payment-success.html")


def payment_failed(request):

    return render(request, template_name="donation/payment-failed.html")
