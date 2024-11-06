# config.py
from web3 import Web3

# Configuration du nœud local Ganache
GANACHE_URL = "http://127.0.0.1:7545"

# Adresse du contrat déployé sur la blockchain
CONTRACT_ADDRESS = "0x9A301686B9a5cBfCfEc20e250fA25B55E1cb7d01"

# Adresse du propriétaire du contrat
OWNER_ADDRESS = "0x419A88794A719245327f323f13afa32ac2B8f621"

# Clé privée pour signer les transactions (à utiliser uniquement pour les tests)
PRIVATE_KEY = "0x65e759351f1e21c4dd8911d3050e50060bd64f5fd136806005edf31be1fd853d"

# Connexion au nœud Ethereum Sepolia
SEPOLIA_URL = "https://rpc.sepolia.org"
w3 = Web3(Web3.HTTPProvider(SEPOLIA_URL))


CRYPTOCOMPARE_API_KEY = "162e3b64f2b558673829f4b0899f7964bfafcfe4a212130389afd08150113be7"


# Vérification de la connexion à la blockchain
if not w3.is_connected():
    raise Exception("Connexion au nœud Ethereum échouée.")
    print("Connexion à Ganache :", w3.isConnected())
