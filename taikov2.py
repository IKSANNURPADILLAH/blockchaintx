from web3 import Web3, HTTPProvider
import json

RPC_URL = "https://rpc.ankr.com/taiko"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

chainId = web3.eth.chain_id

# Menghubungkan web3
if web3.is_connected():
    print("Web3 Connected...\n")
else:
    print("Error Connecting Please Try Again...")
    exit()

print('Auto TX Fast Taiko | @ylasgamers')
print('')

# Meminta input dari pengguna untuk jumlah transaksi maksimal
max_transactions = int(input("Input maximum number of transactions: "))

voteaddr = web3.to_checksum_address("0x4D1E2145082d0AB0fDa4a973dC4887C7295e21aB")
voteabi = json.loads('[{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"vote","outputs":[],"stateMutability":"payable","type":"function"}]')
vote_contract = web3.eth.contract(address=voteaddr, abi=voteabi)

# Variabel untuk menghitung jumlah transaksi
transaction_count = 0

def vote(wallet, key):
    global transaction_count
    try:
        for i in range(15):
            if transaction_count >= max_transactions:
                print(f'Transaction limit {max_transactions} reached. Stopping...')
                return
            nonce = web3.eth.get_transaction_count(wallet) + i
            gasAmount = vote_contract.functions.vote().estimate_gas({
                'chainId': chainId,
                'from': wallet
            })
            gasPrice = 5050 / gasAmount
            votetx = vote_contract.functions.vote().build_transaction({
                'chainId': chainId,
                'from': wallet,
                'gas': gasAmount,
                'maxFeePerGas': web3.to_wei(gasPrice, 'gwei'),
                'maxPriorityFeePerGas': web3.to_wei(gasPrice, 'gwei'),
                'nonce': nonce
            })
            # Sign & send the transaction
            print(f'Processing Vote For Wallet Address {wallet} ...')
            tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(votetx, key).rawTransaction)
            print(f'Processing Vote Success!')
            print(f'TX-ID : {web3.to_hex(tx_hash)}')
            print(f'')
            transaction_count += 1
    except Exception as e:
        print(f'Error: {e}')
        print('Will Try Again...')
        pass

while transaction_count < max_transactions:
    with open('pvkeylist.txt', 'r') as file:
        pvkeylist = file.read().splitlines()
        for loadkey in pvkeylist:
            wallet = web3.eth.account.from_key(loadkey)
            vote(wallet.address, wallet.key)
            if transaction_count >= max_transactions:
                break
