from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid
import time

from .models import Donation


def my_donation(request):

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

    context = {
        'paypal_form': paypal_form
    }

    return render(request, template_name="donation/my-donation.html", context=context)


def payment_success(request):

    # time.sleep(10) # for ngrok

    return render(request, template_name="donation/payment-success.html")


def payment_failed(request):

    return render(request, template_name="donation/payment-failed.html")
