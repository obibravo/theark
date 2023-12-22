# ethereum_webhook/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3
import json
from .models import EthereumTransaction

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


from web3 import Web3

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

        # Get the transaction count (number of transactions) for the wallet address
        wallet_address = '0x12AE66CDc592e10B60f9097a7b0D3C59fce29876'
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
