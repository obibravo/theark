# multitenant/tenants/urls.py
from django.urls import path
from .views import *

app_name = 'walletoverlap'


urlpatterns = [
    path('ethereum-webhook/', ethereum_webhook, name='ethereum_webhook'),
    path('get-real-time-transactions/', get_real_time_transactions, name='get_real_time_transactions'),
    path('get_wallet_transactions/', get_wallet_transactions, name='get_wallet_transactions'),
]
