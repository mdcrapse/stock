document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("teamChart");
  const graph = new graphology.Graph();

  // 1. Create central team node
  graph.addNode("team_root", {
    label: "Team",
    x: 0,
    y: 0,
    size: 25,
    color: "#ff4757",
  });

  /**
   * Adds a certain amount of nodes around the center node
   * @param {number} count - Number of user nodes to add
   * @param {number} radius - Distance from the center
   */
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
        color: "#2e86de",
      });

      // Draw connection to the center team node
      graph.addEdge("team_root", nodeId, {
        size: 2,
        color: "#ced4da",
      });
    }
  }

  // 2. Populate the graph
  populateTeam(12, 5);

  // 3. Render via Sigma
  const sigmaInstance = new Sigma(graph, container, {
    renderLabels: true,
    labelSize: 14,
  });

  // 4. Show the wrapper
  const wrapper = document.getElementById("chartWrapper");
  if (wrapper) {
    wrapper.style.display = "block";
  }
});