const ProjectListing = artifacts.require("ProjectListing");

module.exports = function (deployer) {
    const requiredVotes = 10; // Ou toute autre valeur souhaitée
    deployer.deploy(ProjectListing, requiredVotes);
};
