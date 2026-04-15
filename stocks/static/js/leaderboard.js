document.addEventListener("DOMContentLoaded", () => {
    populateGraph();
});

async function populateGraph() {
    const url = "/leaderboard/top_teams";
    const container = document.getElementById("teamsChart");
    const graph = new graphology.Graph();
    let result = { result: "bad" };

    try {
        const response = await fetch(url);
        result = await response.json();
    } catch(e) {
        console.error(e);
        return;
    }

    // Create central node
    graph.addNode("graph_root", {
        label: "H-Index Teams",
        x: 0,
        y: 0,
        size: 25,
        color: "#ff4757",
    });

    function populateTeams(names, team_data) {
        const angleOffset = 0;//Math.random() * (3);
        const count = names.length;
        let i = 0;
        for(const name of names) {
            const nodeId = name;
            const angle = angleOffset + (i * 2 * Math.PI) / count;

            const dynamicRadius = 5 + (names.length * 1.5);

            const posX = dynamicRadius * Math.cos(angle);
            const posY = dynamicRadius * Math.sin(angle);

            // Add the team node
            graph.addNode(nodeId, {
                label: name,
                x: posX,
                y: posY,
                size: 15,
                color: "#2e86de",
            });

            graph.addEdge("graph_root", nodeId, {
                size: 2,
                color: "#ced4da",
            });

            populateStocks(name, posX, posY, team_data);

            i++;
        }
    }

    function populateStocks(parent_name, parent_posX, parent_posY, team_data, radius = 3) {
        for(const team in team_data) {
            // Skip over non relevant tickers
            if(team != parent_name) {
                continue;
            }

            stocks = team_data[team];
            const count = stocks.length;
            const angleOffset = 0;//Math.random() * (3);
            let i = 0;
            for(const stock of stocks) {
                const nodeId = `${parent_name}-${stock.ticker}`;
                const angle = angleOffset + (i * 2 * Math.PI) / count;

                const posX = parent_posX + (radius * Math.cos(angle));
                const posY = parent_posY + (radius * Math.sin(angle));

                // Add the team node
                graph.addNode(nodeId, {
                    label: stock.ticker,
                    x: posX,
                    y: posY,
                    size: 10,
                    color: "#2ede7d",
                });

                graph.addEdge(parent_name, nodeId, {
                    size: 2,
                    color: "#ced4da",
                });

                i++;
            }
            
        }
    }

    team_data = result.team_stocks;
    names = Object.keys(team_data);
    populateTeams(names, team_data);

    let s;

    s = new Sigma(graph, container, {
        renderLabels: true,
        labelSize: 14,
        labelRenderedSizeThreshold: 12,
        nodeReducer: (node, data) => {
            const res = { ...data };
            
            if (typeof s !== "undefined") {
                const ratio = s.getCamera().getState().ratio;

                if (data.color === "#2ede7d" && ratio > 0.5) {
                    res.hidden = true;
                    res.label = "";
                }
            }

            return res;
        },

        edgeReducer: (edge, data) => {
            const res = { ...data };
            if (typeof s !== "undefined") {
                const ratio = s.getCamera().getState().ratio;
                if (ratio > 0.5 && edge.includes("-")) {
                    res.hidden = true;
                }
            }
            return res;
        }
    });

    s.getCamera().on("updated", () => {
        s.refresh();
    });

    s.refresh();
}