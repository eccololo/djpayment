from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid


def my_donation(request):

    # get the current host of requested website
    host = request.get_host()

    # paypal dict with PayPal API keys.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 5, # 5 USD
        'item_name': 'Donate to Charity',
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

    return render(request, template_name="donation/payment-success.html")


def payment_failed(request):

    return render(request, template_name="donation/payment-failed.html")
