// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProjectListing {
    // Déclaration de l'événement
    event Voted(address indexed voter, uint indexed projectId, uint amount);
    
    struct Project {
        uint id;
        string name;
        string description;
        uint totalTokensSold;
        uint votes;
        bool isActive;
        uint deadline;
    }

    mapping(uint => Project) public projects;
    uint public nextProjectId;
    address public owner;
    uint256 public requiredVotes; // Déclaration de la variable

    // Constructeur avec initialisation de requiredVotes
    constructor(uint256 _requiredVotes) {
        owner = msg.sender;
        requiredVotes = _requiredVotes; // Initialisation dans le constructeur
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    // Ajouter un projet
    function addProject(string memory _name, string memory _description, uint _deadline) public onlyOwner {
        require(_deadline > block.timestamp, "Deadline should be in the future");
        projects[nextProjectId] = Project(nextProjectId, _name, _description, 0, 0, true, _deadline);
        nextProjectId++;
    }

    function vote(uint _projectId, uint _amount) public {
        require(projects[_projectId].isActive, "Project not active");
        require(block.timestamp < projects[_projectId].deadline, "Voting has ended for this project");
        require(_amount > 0, "Amount must be greater than 0");

        // Assurez-vous que l'utilisateur a suffisamment de tokens pour voter
        // Ici, vous pouvez ajouter la logique pour transférer des tokens si vous en avez un contrat de token ERC20
        // token.transferFrom(msg.sender, address(this), _amount);

        projects[_projectId].totalTokensSold += _amount;
        projects[_projectId].votes += _amount;

        // Événements pour suivre les votes (facultatif)
        emit Voted(msg.sender, _projectId, _amount);
    }

    // Get sorted list of projects after the deadline
    function getProjectsSortedByVotes() public view returns (Project[] memory) {
        uint count = nextProjectId;
        Project[] memory sortedProjects = new Project[](count);
        for (uint i = 0; i < count; i++) {
            sortedProjects[i] = projects[i];
        }
        // Simple bubble sort for demonstration (not efficient for large lists)
        for (uint i = 0; i < count; i++) {
            for (uint j = i + 1; j < count; j++) {
                if (sortedProjects[i].votes < sortedProjects[j].votes) {
                    Project memory temp = sortedProjects[i];
                    sortedProjects[i] = sortedProjects[j];
                    sortedProjects[j] = temp;
                }
            }
        }
        return sortedProjects;
    }

    // Remboursement en cas d'échec
    function refund(uint256 projectId) public {
        require(projectId < nextProjectId, "Project does not exist");
        Project storage project = projects[projectId];
        require(block.timestamp > project.deadline, "Deadline has not passed");
        require(project.votes < 100, "Project has enough votes, not eligible for refund");

        // Logique de remboursement
        project.votes = 0; // Réinitialiser le nombre de votes
        project.isActive = false; // Désactive le projet
        project.totalTokensSold = 0; // Réinitialise les tokens vendus
        
    }


}
