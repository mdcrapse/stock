// Expects `member_names` to exist in the global context.
// This is done to avoid needing to request the names after the webpage is loaded.
// `member_names` should be an array of strings.
document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("teamChart");
  const graph = new graphology.Graph();

  // Create central team node
  graph.addNode("team_root", {
    label: "Team",
    x: 0,
    y: 0,
    size: 25,
    color: "#ff4757",
  });

  /**
   * Adds a certain amount of nodes around the center node
   * @param {string[]} names - User node names to add
   * @param {number} radius - Distance from the center
   */
  function populateTeam(names, radius = 10) {
    const count = names.length;
    let i = 0;
    for (const name of names) {
      const nodeId = name;
      const angle = (i * 2 * Math.PI) / count;

      const posX = radius * Math.cos(angle);
      const posY = radius * Math.sin(angle);

      // Add User Node
      graph.addNode(nodeId, {
        label: name,
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

      i++;
    }
  }

  // Populate the graph
  populateTeam(member_names, 5);

  // Render via Sigma
  const sigmaInstance = new Sigma(graph, container, {
    renderLabels: true,
    labelSize: 14,
  });

  // Show the wrapper
  const wrapper = document.getElementById("chartWrapper");
  if (wrapper) {
    wrapper.style.display = "block";
  }
});