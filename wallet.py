from constants import *
import os
from dotenv import load_dotenv
import subprocess
import json
from eth_account import Account
from bit import PrivateKeyTestnet


# instantiate variables and objects
# coins object to derive desired wallets
coins = {
    BTCTEST: '',
    ETH: ''
}

# load .env environment variables
load_dotenv()

# set the mnemonic as an environment variable
mnemonic = os.getenv('MNEMONIC')

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

# to generate multiple keys and fill coins object
for coin in coins:
    coins[coin] = derive_wallets(mnemonic, coin, 3)


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

value = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
print(value)
