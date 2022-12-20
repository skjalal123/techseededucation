from django.conf.urls import include, url
from django.contrib import admin
from Payment.views import *

urlpatterns = [
    url(r'^cart/', Payment.as_view()),
    url(r'^cartview/', CartView.as_view()),
    url(r'^paymentapiresponse', PaymentAPIResponse.as_view()),
]
