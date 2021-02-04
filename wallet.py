from constants import *
import os
from dotenv import load_dotenv
import subprocess
import json
from eth_account import Account
from bit import PrivateKeyTestnet
from web3 import Web3

# instantiate variables and objects
# coins object to derive desired wallets
mnemonic = 'na'
coins = {
    BTCTEST: '',
    ETH: ''
}

# load .env environment variables
load_dotenv()

# set the mnemonic as an environment variable
mnemonic = os.getenv('MNEMONIC')

# test for mnemonic phrase
if mnemonic == 'na':
    print("Please check your .env file for your mnemonic phrase.  No mnemonic phrase found.")
    quit()

def derive_wallets(mnemonic_string, coin, num_to_derive):
    """Derives wallet keys based on a single mnemonic string
    Args:
        mnemonic_string (str): Mnemonic string of phrases to use
        coin (str): Coin to generate keys in (example: BTC, BTCTEST, ETH, etc.)
        num_to_derive (int): Number of child keys to derive
    Returns:
        JSON object with path, address, private keys and public keys
    """
    # create command line to generate keys
    command = f'php derive -g --mnemonic="{mnemonic_string}" --coin={coin} --numderive={num_to_derive} --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'
    
    # call the command line to process script
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    # parse the output into a json object
    keys = json.loads(output)
    return keys

def generate_and_derive_wallets(coin_dict, mnemonic, num_keys):
    """Generates and derives wallets
    Args:
        coin_dict (dictionary): Dictionary containing coins
        mnemonic (str): Mnemonic string of phrases to use
        num_keys (int): Number of child keys to create for each coin
    Returns:
        Dictionary of coins and keys
    """
    # to generate multiple keys and fill coins object
    for coin in coin_dict:
        # derive wallet with keys
        coin_dict[coin] = derive_wallets(mnemonic, coin, num_keys)
    return coin_dict

def priv_key_to_account(coin, priv_key):
    """Will convert the private key string in a child key to an account object
    Args:
        coin (str): The coin type defined in constants.py
        priv_key (str): The private key of the coin
    Returns:
        An account private key.  If converting BTCTEST, will return a Wallet
        Import Format (WIF) object.
    """
    # check the coin for ETH
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    # check the coin for BTCTEST
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


coins = generate_and_derive_wallets(coins, mnemonic, 3)

'''
def create_tx(coin, account, to, amount):
    """This will create the raw, unsigned transaction that contains all metadata 
    needed to transact
    Args:
        coin (str): The coin type defined in constants.py
        account (obj): The account object from priv_key_to_account()
        to (str): The recipient address
        amount (flt): The amount of the coin to send
    Returns:
        A dictionary of values: to, from, value, gas, gasPrice, nonce and chainID
    """
'''

coin = BTCTEST
account = priv_key_to_account(coin, coins[coin][2]['privkey'])
to = '0xbfB60ca3E4a18baC3BA44630bD2449DCAB349b56'
amount = 9999999

# create connection for Web3 communication
connection = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# check the coin for ETH
if coin == ETH:
    # estimate gas price for transaction
    gasEstimate = connection.eth.estimateGas({
        "from": account.address,
        "to": to,
        "value": amount
    })
    # return necessary data for transaction
    returned_val = {
        'from': account.address,
        'to': to,
        'value': amount,
        'gasPrice': gasEstimate,
        'nonce': connection.eth.getTransactionCount(account.address),
        'chainID': connection.eth.chainId
    }
if coin == BTCTEST:
    returned_val = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

print(returned_val)
