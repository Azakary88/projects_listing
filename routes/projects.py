
from flask import Blueprint, jsonify, request, render_template
from models import contract, w3
from datetime import datetime
import time

projects_bp = Blueprint('projects_bp', __name__)



@projects_bp.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        data = request.get_json()

        # Vérification des données reçues
        print("Données reçues :", data)

        # Vérifier que 'deadline' est présent dans les données reçues
        if 'deadline' not in data:
            return jsonify({"error": "Le champ deadline est requis"}), 400

        # Convertir le 'deadline' en entier et l'ajouter au temps actuel
        try:
            deadline_seconds = int(data['deadline'])
            current_time = int(time.time())  # Obtenir l'heure actuelle en secondes
            deadline = current_time + deadline_seconds
        except ValueError:
            return jsonify({"error": "Le champ deadline doit être un nombre entier"}), 400

        # Vérifier si le deadline est dans le futur
        if deadline <= current_time:
            return jsonify({"error": "Le champ deadline doit être une date future"}), 400

        # Appel de la fonction addProject avec les arguments correctement typés
        tx = contract.functions.addProject(data['name'], data['description'], deadline).transact({
            'from': w3.eth.accounts[0],
            'gas': 1000000
        })
        w3.eth.wait_for_transaction_receipt(tx)

        return jsonify({"message": "Projet ajouté avec succès"}), 201

    # Si la méthode est GET, afficher le formulaire
    return render_template('add_project.html')


@projects_bp.route('/list', methods=['GET'])
def list_projects():
    next_project_id = contract.functions.nextProjectId().call()
    projects = []
    for i in range(next_project_id):
        project = contract.functions.projects(i).call()
        projects.append({
            "id": project[0],
            "name": project[1],
            "description": project[2],
            "totalTokensSold": project[3],
            "votes": project[4],
            "isActive": project[5],
            "deadline": project[6]
        })
    return render_template('projects_list.html', projects=projects)
