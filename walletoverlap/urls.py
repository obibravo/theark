# multitenant/tenants/urls.py
from django.urls import path
from .views import *

app_name = 'walletoverlap'


urlpatterns = [
    path('etherscan/<str:wallet_address>/', etherscan, name='etherscan'),
    path('overlap/<str:wallet_address>/', overlap, name='overlap'),
    # path('ethplorer/', ethplorer, name='ethplorer'),
    path('all_overlap/', all_overlap, name='all_overlap'),
    path('ethplorer_address_info/', ethplorer_address_info, name='ethplorer_address_info'),
    path('ethplorer_address_info/<str:wallet_address>/', ethplorer_address_info_with_address, name='ethplorer_address_info_with_address'),
    path('website/', website, name='website'),
]
