import subprocess
import json
from constants import *
import os
from dotenv import load_dotenv

# load .env environment variables
load_dotenv()

# set the mnemonic as an environment variable with a fallback
mnemonic = os.getenv('MNEMONIC', 'balcony defense hurdle paddle crazy vivid decorate blast behind heavy exchange fat')

command = './derive -g --mnemonic="INSERT HERE" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
