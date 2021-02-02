import subprocess
import json
from constants import *
import os
from dotenv import load_dotenv

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
    Arg:
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


#for coin in coins:
keys = derive_wallets(mnemonic, coins, 3)

print(keys)
