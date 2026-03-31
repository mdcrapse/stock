document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("teamChart");
    const graph = new graphology.Graph();

    // Create central team node
    graph.addNode("team_root", { 
        label: "Team", 
        x: 0, 
        y: 0, 
        size: 25, 
        color: "#ff4757" 
    });

    // Adds a certain amount of nodes around the center node
    function populateTeam(count, radius = 10) {
        for (let i = 0; i < count; i++) {
            const nodeId = `user_${i}`;
            const angle = (i * 2 * Math.PI) / count;

            const posX = radius * Math.cos(angle);
            const posY = radius * Math.sin(angle);

            // Add User Node
            graph.addNode(nodeId, {
                label: `User ${i + 1}`,
                x: posX,
                y: posY,
                size: 12,
                color: "#2e86de"
            });

            // Draw connection to the center team node
            graph.addEdge("team_root", nodeId, { 
                size: 2, 
                color: "#ced4da" 
            });
        }
    }

    // Populate the graph
    populateTeam(12, 5);

    // REnder
    const sigmaInstance = new Sigma(graph, container, {
        renderLabels: true,
        labelSize: 14
    });

    // Show the wrapper
    document.getElementById('chartWrapper').style.display = 'block';
});