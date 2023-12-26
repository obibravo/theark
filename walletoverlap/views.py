# ethereum_webhook/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from web3 import Web3
import json
from .models import EthereumTransaction, Token, Wallet

@csrf_exempt
def ethereum_webhook(request):
    pass
    # ... (existing code)

def get_real_time_transactions(request):
    try:
        # Connect to an Ethereum node (replace 'http://your-ethereum-node-url' with an actual node URL)
        w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/h6ixsVSdhsgyM_edF3zzDIfATY3DU57e'))

        # Get the latest block number
        latest_block_number = w3.eth.blockNumber

        # Get transactions from the latest block
        transactions = w3.eth.get_block(latest_block_number)['transactions']
        print(transactions)

        # Process and save transactions to the database
        for tx_hash in transactions:
            tx = w3.eth.get_transaction(tx_hash)
            from_address = tx['from']
            to_address = tx['to']
            value = w3.fromWei(tx['value'], 'ether')

            EthereumTransaction.objects.create(
                transaction_hash=tx_hash,
                from_address=from_address,
                to_address=to_address,
                value=value
            )

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# from web3 import Web3

def get_wallet_transactions(request):
    try:
        wallet_address=None; node_url='https://eth-mainnet.g.alchemy.com/v2/h6ixsVSdhsgyM_edF3zzDlfATY3DU57e'
        # Connect to the Ethereum node
        print(1333)
        w3 = Web3(Web3.HTTPProvider(node_url))
        print(1222)

        # Ensure the node is connected
        # if not w3.isConnected():
        #     return JsonResponse({'status': 'error', 'message': 'Unable to connect to Ethereum node'})
        wallet_address = '0x12AE66CDc592e10B60f9097a7b0D3C59fce29876'
        real_ethereum_address='0x03770b07c5c315722c5866e64cde04e6e5793714'

        usdt_contract_abi = [
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "Transfer",
    "type": "event"
  }


            # Include the ABI of the USDT contract. You can obtain this from the Ethereum contract source code or other reliable sources.
        ]

        # Create contract instance
        usdt_contract = w3.eth.contract(address=wallet_address, abi=usdt_contract_abi)

        # Ethereum address to check for USDT transactions
        target_address = '0x12AE66CDc592e10B60f9097a7b0D3C59fce29876'
        print(w3.eth.get_transaction(555555))
        

        contract = w3.eth.contract(address=wallet_address, abi=abi)
        
        result = w3.eth.get_transaction(txhash)
        func_obj, func_params = contract.decode_function_input(result["input"])
        print (result["input"])
        print(func_params)


        # Get USDT transfer events for the target address
        usdt_transfers = usdt_contract.events.Transfer().getLogs(
            {
                'fromBlock': 0,
                'toBlock': 'latest',
                # 'filter': {
                #     'from': target_address,
                # },
            }
        )
        print(usdt_transfers)

        # Get the transaction count (number of transactions) for the wallet address
        checksum_address = w3.to_checksum_address(wallet_address)
        print(1)
        transaction_count = w3.eth.get_transaction_count(wallet_address)
        print(12)
        tx_hash = w3.eth.get_transaction_receipt('0xe2dd28160e480d1a4b95152b00cfd507749474ea2712d9fe575beec88e0d7d10')
        print(tx_hash)

        # Get the list of transactions
        transactions = []
        for i in range(transaction_count):
            # Get transaction hash
            tx_hash = w3.eth.get_transaction_receipt(wallet_address)
            tx_hash = w3.eth.get_transaction_by_block(w3.eth.get_block, i)['hash']
            tx = w3.eth.getTransaction(tx_hash)

            # Extract relevant transaction data
            transaction_data = {
                'hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'value': w3.fromWei(tx['value'], 'ether'),
                'gas_price': w3.fromWei(tx['gasPrice'], 'gwei'),
                'timestamp': w3.eth.getBlock(tx['blockNumber'])['timestamp'],
            }

            transactions.append(transaction_data)

        return JsonResponse({'status': 'success', 'transactions': transactions})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Example usage
# wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714'
# result = get_wallet_transactions(wallet_address)

# print(result)

import requests


def etherscan(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714'):
    # Your Etherscan API key
    api_key = '28XVCAQXKFI2GN8GGB3SFHMVQ3XS2XTXK5'

    # Ethereum address to check for transaction details
    

    # Define the Etherscan API endpoint
    api_endpoint = f'https://api.etherscan.io/api'

    # Set the action to 'txlist' to get the list of transactions
    action = 'txlist'

    # Make the API request
    params = {
        'module': 'account',
        'action': action,
        'address': wallet_address,
        'apikey': api_key,
    }

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
            print("Transaction Hash:", tx['hash'])
            print("Block Number:", tx['blockNumber'])
            print("Timestamp:", tx['timeStamp'])
            print("From:", tx['from'])
            print("To:", tx['to'])
            print("Value in Ether:", float(tx['value']) / 1e18)
            print("Gas Price:", float(tx['gasPrice']) / 1e9  , "Gwei")
            print("--------------------")


            # user = form.cleaned_data['user']
            wallet_name =wallet_address
            wallet_address = wallet_address
            wallet_balance =0
            token_name = wallet_address
            token_address =  tx['hash']
            token_balance =0
            token_quantity =  float(float(tx['value']) / 1e18)

            # Create and save Wallet instance
            print(wallet)
            iter+=1

            # Create and save Token instance with the associated Wallet
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

    else:
        print("Failed to retrieve transaction details. Check your API key or try again later.")
        print("Error Message:", data['message'])
    print(len(data))
    return  JsonResponse({'data': data})

from django.db.models import Sum
from django.core.serializers import serialize

def overlap(request,wallet_address = '0x03770b07c5c315722c5866e64cde04e6e5793714'):
    template_name = 'your_template.html'

    # Retrieve the wallet
    wallet = Wallet.objects.get(address=wallet_address)

    # Retrieve tokens for the wallet and calculate the sum of quantities
    token_sum = Token.objects.filter(wallet=wallet).aggregate(Sum('quantity'))['quantity__sum']

    # Optionally, you can retrieve the individual tokens as well
    tokens = Token.objects.filter(wallet=wallet)
    tokens_quantity=[]
    for i in tokens:tokens_quantity.append([i.token_address ,i.quantity])
    context={'wallet': wallet.name, 'token_sum': str(token_sum)+' in ether', 'tokens':tokens_quantity
        #serialize('json', [str(i.quantity) for i in tokens ])
             }
    return  JsonResponse({'context': context})
    # return render(request, template_name, context)