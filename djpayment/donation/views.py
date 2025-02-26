from django.shortcuts import render


def my_donation(request):

    return render(request, template_name="donation/my-donation.html")


def payment_success(request):

    return render(request, template_name="donation/payment-success.html")


def payment_failed(request):

    return render(request, template_name="donation/payment-failed.html")
