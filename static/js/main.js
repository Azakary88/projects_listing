// static/js/main.js
import Web3 from 'web3'; 

document.addEventListener('DOMContentLoaded', () => {
    if (typeof Web3 !== 'undefined') {
        // Web3 est disponible
        const web3 = new Web3(window.ethereum); // ou window.web3.currentProvider si vous utilisez un fournisseur hérité
        console.log('Web3 initialisé');
    } else {
        console.error('Web3 non trouvé');
    }

    let web3;
    let userAddress;
    let contract;

   
    // Connexion à MetaMask
async function connectWallet() {
    if (window.ethereum) {
        try {
            // Demander la connexion du compte utilisateur
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            userAddress = accounts[0];
            web3 = new Web3(window.ethereum);
            console.log('Adresse du wallet:', userAddress);
            console.log('Objet Web3:', web3);
            alert('Wallet connecté avec succès: ' + userAddress);
            
            // Écouter l'événement 'disconnect' pour gérer les déconnexions
            window.ethereum.on('disconnect', (error) => {
                console.log('MetaMask déconnecté', error);
                alert("Vous avez été déconnecté de MetaMask.");
                // Réinitialiser les variables si nécessaire
                userAddress = null;
                web3 = null;
                contract = null;
            });

            // Charger le contrat après la connexion
            await loadContract(); 
        } catch (error) {
            console.error('Erreur lors de la connexion:', error);
        }
    } else {
        alert("MetaMask n'est pas installé. Veuillez l'installer pour continuer.");
    }
}


    // Charger l'ABI et créer l'instance du contrat
    async function loadContract() {
        const contractABI = await fetch('/static/js/ABI.json').then(response => response.json());
        const contractAddress = "0x1eA95322aDc64ed81dB63339A791e66734A0d078"; // Remplacez par l'adresse de votre contrat
        contract = new web3.eth.Contract(contractABI, contractAddress);
        console.log("Contrat chargé :", contract);
    }

    // Fonction pour ajouter un projet
    async function addProject() {
        if (!web3 || !userAddress) {
            alert("Veuillez connecter votre wallet avant d'ajouter un projet.");
            return;
        }
        
        const name = prompt('Entrez le nom du projet:');
        const description = prompt('Entrez la description du projet:');
        const deadline = prompt('Entrez la date limite du projet (en timestamp UNIX):');
    
        if (!name || !description || !deadline) {
            alert('Tous les champs sont requis.');
            return;
        }

        try {
            await contract.methods.addProject(name, description, deadline).send({ from: userAddress });
            alert('Projet ajouté avec succès!');
        } catch (error) {
            console.error('Erreur lors de l\'ajout du projet:', error);
        }
    }

    // Fonction pour acheter des tokens (voter)
    async function buyTokens() {
        const projectId = document.getElementById('project-id').value;
        const tokenAmount = document.getElementById('token-amount').value;

        if (!web3 || !userAddress) {
            alert("Veuillez connecter votre wallet avant de voter.");
            return;
        }

        if (!projectId || !tokenAmount) {
            alert("Veuillez entrer l'ID du projet et le nombre de tokens.");
            return;
        }

        try {
            // Appeler la fonction de vote avec le montant de tokens
            await contract.methods.vote(projectId, tokenAmount).send({ from: userAddress });
            alert("Vote enregistré avec succès !");
        } catch (error) {
            console.error("Erreur lors de l'achat de tokens :", error);
            alert("Erreur lors du vote.");
        }
    }

    // Ajouter les écouteurs d'événements
    document.getElementById('connect-wallet').addEventListener('click', connectWallet);
    document.getElementById('add-project').addEventListener('click', addProject);
    document.getElementById('vote-button').addEventListener('click', buyTokens);
});
