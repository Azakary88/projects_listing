# models.py
from web3 import Web3
from blockchain import config
from blockchain import contract
import requests
from blockchain.config import CRYPTOCOMPARE_API_KEY
import json

# Connexion à Ganache
w3 = Web3(Web3.HTTPProvider(config.GANACHE_URL))

# Charger l'ABI
with open("build/contracts/ProjectListing.json") as f:
    contract_abi = json.load(f)["abi"]

# Adresse du contrat
contract_address = config.CONTRACT_ADDRESS

# Créer une instance du contrat
contract = w3.eth.contract(address=contract_address, abi=contract_abi)



def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    headers = {
        "authorization": f"Apikey {CRYPTOCOMPARE_API_KEY}"
    }
    params = {
        "lang": "FR"  # Code pour la langue française
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        news_data = response.json()["Data"]
        return news_data
    else:
        print(f"Erreur lors de la récupération des actualités: {response.status_code}")
        return []

# Exemple d’utilisation
news_list = get_crypto_news()
for article in news_list:
    print(article["title"], "-", article["body"])

