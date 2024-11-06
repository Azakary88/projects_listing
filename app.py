from flask import Flask, render_template
from routes.projects import projects_bp
from routes.votes import votes_bp
from blockchain.config import GANACHE_URL, CONTRACT_ADDRESS, OWNER_ADDRESS, PRIVATE_KEY, w3, CRYPTOCOMPARE_API_KEY
from blockchain.contract import contract
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration de l'application
app.config['GANACHE_URL'] = GANACHE_URL
app.config['CONTRACT_ADDRESS'] = CONTRACT_ADDRESS
app.config['OWNER_ADDRESS'] = OWNER_ADDRESS
app.config['PRIVATE_KEY'] = PRIVATE_KEY

# Enregistrement des blueprints avec des préfixes uniques
app.register_blueprint(projects_bp, url_prefix='/projects')
app.register_blueprint(votes_bp, url_prefix='/votes')

# Route d'accueil pour vérifier que l'application fonctionne
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_project', methods=['GET'])
def add_project():
    return render_template('add_project.html')

@app.route("/blockchain-news")
def blockchain_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    headers = {
        "authorization": f"Apikey {CRYPTOCOMPARE_API_KEY}"
    }
    params = {
        "lang": "FR"  # Spécifie la langue française
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        news_data = response.json().get("Data", [])  # Utilise .get() pour éviter les erreurs
    else:
        print(f"Erreur lors de la récupération des actualités: {response.status_code}")
        news_data = []  # Retourne une liste vide en cas d'erreur

    return render_template("blockchain_news.html", news=news_data)


if __name__ == '__main__':
    app.run(debug=True)