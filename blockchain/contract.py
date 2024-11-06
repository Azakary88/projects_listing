import json
from web3 import Web3
from blockchain.config import GANACHE_URL, CONTRACT_ADDRESS

# Connexion à Web3
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Charger le fichier ABI
try:
    with open("build/contracts/ProjectListing.json") as f:
        contract_data = json.load(f)  # Charger le contenu du fichier JSON dans contract_data
except FileNotFoundError:
    print("Le fichier 'ProjectListing.json' n'a pas été trouvé.")
    raise

# Vérifier si contract_data est bien défini et contient la clé 'abi'
if 'abi' not in contract_data:
    raise KeyError("'abi' n'est pas présent dans le fichier JSON.")

# Extraire uniquement la liste ABI
contract_abi = contract_data['abi']

# Créer l'objet contrat en utilisant l'ABI extraite
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
