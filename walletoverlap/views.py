from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import EthereumTransaction, Token, Wallet
import requests

def website(request,template=None):
    if template is not None: template=template
    else: template='templates/index.html'
    context=all_overlap(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714',return_dict=True)
    return render(request,template,context)


def etherscan(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714'):
    api_key = '28XVCAQXKFI2GN8GGB3SFHMVQ3XS2XTXK5'
    api_endpoint = f'https://api.etherscan.io/api'
    action = 'txlist'
    params = { 'module': 'account','action': action,
        'address': wallet_address,'apikey': api_key,    }

    response = requests.get(api_endpoint, params=params)
    data = response.json()

    # Check if the request was successful
    if data['status'] == '1':
        # Print transaction details
        wallet = Wallet.objects.get_or_create(
            name=wallet_address,
            address=wallet_address,
            balance=0
        )
        try:wallet.save()
        except:pass
        iter=0
        for tx in data['result']:
            #print("Transaction Hash:", tx['hash'])
            #print("Block Number:", tx['blockNumber'])
            #print("Timestamp:", tx['timeStamp'])
            #print("From:", tx['from'])
            #print("To:", tx['to'])
            #print("Value in Ether:", float(tx['value']) / 1e18)
            #print("Gas Price:", float(tx['gasPrice']) / 1e9  , "Gwei")
            #print("--------------------")


            # user = form.cleaned_data['user']
            wallet_name =wallet_address
            wallet_address = wallet_address
            wallet_balance =0
            token_name = wallet_address
            token_address =  tx['hash']
            token_balance =0
            token_quantity =  float(float(tx['value']) / 1e18)
            ##print(wallet)
            iter+=1
            try:
                token = Token.objects.create(
                    wallet=wallet[0],
                    token_name=token_name +str(iter),
                    token_address=token_address+str(iter),
                    token_balance=token_balance,
                    quantity=token_quantity
                )
                token.save()
            except:pass

    else:pass
        #print("Failed to retrieve transaction details. Check your API key or try again later.")
        #print("Error Message:", data['message'])
    #print(len(data))
    return  JsonResponse({'data': data})

def ethplorer_address_info(request,wallet_address = '0xc1b2c7b19b745e2d07d3a25259f340ae61b8febb'):
    api_endpoint = f'https://api.ethplorer.io/getAddressInfo/{wallet_address}?apiKey=freekey'
    m='https://api.ethplorer.io/getAddressInfo/0xc1b2c7b19b745e2d07d3a25259f340ae61b8febb?apiKey=freekey'

    response = requests.get(api_endpoint )
    data = response.json()
    token_details=[]
    wallet = Wallet.objects.get_or_create(
        name=wallet_address,
        address=wallet_address,
        balance=0
    )
    try:wallet.save()
    except:pass
    failed_token=[]
    for i in data['tokens']:
        tokenInfo=i['tokenInfo']
        try:decimals=tokenInfo['decimals']
        except:decimals=0
        token_name=tokenInfo['name']
        address=tokenInfo['address']
        symbol=tokenInfo['symbol']
        rawBalance=int(i['rawBalance'])/int(10** int(decimals))
        try:
            price=tokenInfo['price']['rate']            
            currency=tokenInfo['price']['currency']
            token_initial_price=price * rawBalance
        except:token_initial_price=None;currency=None

        try:
            token = Token.objects.create(
                wallet=wallet[0],
                token_name=token_name , token_address=address,
                token_initial_price=token_initial_price,
                quantity=rawBalance, currency=currency
            )
            token.save()
        except Exception as e:
            m=(str(e), wallet[0].address, token_name , address, token_initial_price, rawBalance, currency )
            failed_token.append(m)

        token_details.append([symbol,decimals,token_name,rawBalance,price,currency])
        #print(token_details,'\n')
    if failed_token!=[]:return  JsonResponse({'total failed_token':failed_token})

    return  JsonResponse({'total failed_token':len(failed_token),'failed_token':failed_token,'token_details':token_details,
                          'data': data,'total tokens':len(data['tokens'])})

def ethplorer_address_info_with_address(request,wallet_address = None):
    return ethplorer_address_info(request,wallet_address = wallet_address)

# def ethplorer(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714'):
#     api_endpoint = f'https://api.ethplorer.io/getTokenInfo/{wallet_address}?apiKey=freekey'
#     api_key='28XVCAQXKFI2GN8GGB3SFHMVQ3XS2XTXK5'
#     api_endpoint=f'https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}'
#     api_endpoint=f'https://api.etherscan.io/api?module=account&action=tokenbalance&address={wallet_address}&sort=asc&apikey={api_key}'
#     #print(api_endpoint)

#     response = requests.get(api_endpoint )
#     data = response.json()
#     #print(data)
#     token_details=[]

#     return  JsonResponse({'token_details':token_details,'data': data})



from django.db.models import Sum

def overlap(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714',return_dict=False):
    template='templates/overlap1.html'
    wallet = Wallet.objects.get(address=wallet_address)
    token_sum = Token.objects.filter(wallet=wallet).aggregate(Sum('token_initial_price'))['token_initial_price__sum']

    tokens = Token.objects.filter(wallet=wallet)
    tokens_quantity=[]
    for i in tokens:
        if i.quantity is not None and i.token_initial_price is not None:
            each_token_price=float(i.quantity)* float(i.token_initial_price)
        else:each_token_price=None
        tokens_quantity+=[{'token_name':i.token_name,'quantity':i.quantity,'token_initial_price':
        i.token_initial_price ,'each_token_price':each_token_price }]
    context={'all_tokens_in_address':{'wallet': wallet.name, 'token_sum': str(token_sum)+' in USD', 'tokens':tokens_quantity,
             'amount_of_token':len(tokens) }  ,'time_created':wallet.time_created          }
    if return_dict==True:
        context={'wallet': wallet.name, 'token_sum': str(token_sum)+' in USD', 'tokens':tokens_quantity,
             'amount_of_token':len(tokens)             }
        return context
    return render(request,template,context)


def all_overlap(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714',return_dict=False):
    all_wallets=Wallet.objects.all()
    all_wallets_dict={}
    all_wallet_list=[]
    for ii in all_wallets:
        wallet_addresses=ii.address
        wallet_info= overlap(request,wallet_address = wallet_addresses,return_dict=True)
        all_wallets_dict={**all_wallets_dict, **wallet_info}
        all_wallet_list.append(all_wallets_dict)
    # #print(all_wallets_dict)
    context={'all_wallets_dict':[{'wallet':oo['wallet'],'token_sum':oo['token_sum'],
                            'amount_of_token':oo['amount_of_token'],'wallets':oo['wallet'] }
                                                        for oo in all_wallet_list],
                                              }
    if return_dict==True:return context
    return  JsonResponse(context)

