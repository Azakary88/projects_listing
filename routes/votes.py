# routes/votes.py
from flask import Blueprint, jsonify, request, render_template
from models import contract, w3

votes_bp = Blueprint('votes_bp', __name__)

@votes_bp.route('/vote', methods=['GET', 'POST'])
def vote():
    print("Route /votes/vote appelée")
    if request.method == 'POST':
        print("Requête POST reçue")
        data = request.get_json()
        print("Données reçues:", data)
        
        # Vérifier les données
        if not data or 'projectId' not in data or 'amount' not in data:
            return jsonify({"error": "Données manquantes"}), 400

        project_id = int(data['projectId'])
        amount = int(data['amount'])

        try:
            # Appel à la fonction vote du contrat
            print(f"Appel à la fonction vote du contrat avec project_id={project_id} et amount={amount}")
            tx = contract.functions.vote(project_id, amount).transact({
                'from': w3.eth.accounts[0],
                'gas': 1000000
            })
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            print("Transaction receipt:", receipt)
            
            # Récupérer la liste mise à jour des projets
            print("Récupération des projets mis à jour")
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

            # Trier les projets par nombre de votes (décroissant)
            projects = sorted(projects, key=lambda x: x["votes"], reverse=True)
            print("Projets triés par votes:", projects)

            return jsonify({"message": "Vote enregistré avec succès", "projects": projects}), 200

        except Exception as e:
            # Gérer des erreurs spécifiques
            error_message = str(e)
            if "Voting has ended" in error_message:
                return jsonify({"error": "Le vote est terminé pour ce projet"}), 400
            elif "insufficient funds" in error_message:
                return jsonify({"error": "Fonds insuffisants pour effectuer ce vote"}), 400
            else:
                print("Erreur lors de l'exécution de la transaction:", e)
                return jsonify({"error": "Erreur lors de la transaction"}), 500

    # GET: affichage du formulaire de vote
    print("Requête GET pour /votes/vote")
    try:
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

        # Trier les projets par nombre de votes (décroissant)
        projects = sorted(projects, key=lambda x: x["votes"], reverse=True)
        print("Projets pour le formulaire de vote:", projects)
        return render_template('vote.html', projects=projects)
    except Exception as e:
        print("Erreur lors de la récupération des projets:", e)
        return render_template('vote.html', projects=[]), 500

@votes_bp.route('/vote-list', methods=['GET'])
def get_vote_list():
    try:
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
        # Trier les projets par nombre de votes
        projects_sorted = sorted(projects, key=lambda x: x["votes"], reverse=True)
        return jsonify({"projects": projects_sorted}), 200
    except Exception as e:
        print("Erreur lors de la récupération des projets triés:", e)
        return jsonify({"error": "Erreur lors de la récupération des projets"}), 500

@votes_bp.route('/refund', methods=['GET', 'POST'])
def refund():
    if request.method == 'POST':
        project_id = request.form.get('projectId')
        
        if project_id:
            try:
                # Convertir l'ID du projet en entier
                project_id = int(project_id)
                
                # Récupérer l'heure actuelle une seule fois
                current_time = w3.eth.get_block('latest').timestamp
                
                # Vérification si le projet existe
                project_data = contract.functions.projects(project_id).call()
                
                # Récupérer le délai du projet et le nombre de votes
                deadline = project_data[6]
                votes = project_data[3]  # Nombre de votes du projet

                # Afficher les informations pour le débogage
                print(f"Project Deadline: {deadline}")
                print(f"Current Time: {current_time}")
                print(f"Project Votes: {votes}")

                # Vérifier si le délai est dépassé
                if current_time < deadline:
                    return render_template('refund.html', message="Le délai n'est pas encore passé. Impossible de rembourser."), 400
                
                # Vérifier le nombre de votes
                if votes >= 100:
                    return render_template('refund.html', message="Le projet a suffisamment de votes. Pas de remboursement autorisé."), 400

                # Appel à la fonction refund du contrat
                tx = contract.functions.refund(project_id).transact({
                    'from': w3.eth.accounts[0],
                    'gas': 1000000
                })
                w3.eth.wait_for_transaction_receipt(tx)

                # Message de succès
                return render_template('refund.html', message="Remboursement effectué avec succès.")
            
            except ValueError:
                return render_template('refund.html', message="L'ID du projet est invalide."), 400
            except Exception as e:
                print(f"Erreur: {e}")
                return render_template('refund.html', message="Erreur lors du traitement de la demande de remboursement."), 400

        return render_template('refund.html', message="ID du projet manquant."), 400

    return render_template('refund.html')



