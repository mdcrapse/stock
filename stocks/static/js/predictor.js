let stockChart = null;

document.getElementById('submit-btn').addEventListener('click', function(){
    // Get references
    const ticker = document.getElementById('ticker_symbol').value;
    const sector = document.getElementById('sector').value;
    const resultContainer = document.getElementById('result-container');
    const resultData = document.getElementById('result-data');
    const alertBox = document.getElementById('alert-box');

    // Show container and loading state
    resultContainer.style.display = 'block';
    resultData.innerHTML = 'Predicting...';
    alertBox.className = 'alert alert-info';

    // Get CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Perform the fetch to the API
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            ticker_symbol: ticker,
            sector: sector
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alertBox.className = 'alert alert-danger';
            resultData.innerHTML = data.error;
        } else {
            if(data.predicted_return > 0)
            {
                alertBox.className = 'alert alert-success';
            } else if(data.predicted_return <= 0){
                alertBox.className = 'alert alert-warning';
            }
            resultData.innerHTML = `
                <p><strong>${data.ticker}</strong> (${data.sector})</p>
                <p>Current Price: $${data.current_price}</p>
                <p>Predicted Return (30d): ${data.predicted_return}</p>
                <p>Predicted Price: $${data.predicted_price}</p>
                <div class="d-flex gap-2 align-items-center justify-content-center">
                    <input type="number" id="num-stocks" class="form-control w-25" placeholder="Amount to Purchase"></input>
                    <button type="button" id="invest-btn" class="btn btn-primary w-25" onclick="validateInvestmentAmount(${data.current_price}, '${data.ticker}')">Invest</button>
                </div>
            `;
        }
        updateChart(data);
    })
    .catch(error => {
        alertBox.className = 'alert alert-danger';
        resultData.innerHTML = 'An error occured. Please try again.';
        console.error('Error:', error);
    });
});

async function validateInvestmentAmount(curPrice, ticker) {
    const numStocks = document.getElementById('num-stocks').value;
    const totalInvestmentCost = numStocks * curPrice;

    // Wait for the balance fetch to finish
    const response = await fetch('/user/get_balance/');
    const data = await response.json();
    const userBalance = data.balance;

    // Unhappy path, alert the user that they don't have sufficient funds
    if (totalInvestmentCost > userBalance) {
        alert("Insuificient funds.");
        return;
    }

    // Happy path, process the investment
    processInvestment(numStocks, ticker, curPrice);
}

function processInvestment(numStocks, ticker, curPrice) {
    const alertBox = document.getElementById('alert-box');
    const resultData = document.getElementById('result-data');
    
    // Get CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Perform the fetch
    fetch('/user/invest/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            symbol: ticker,
            amount: numStocks,
            total_price: numStocks * curPrice
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            alertBox.className = 'alert alert-danger';
            resultData.innerHTML = data.error;
        } else {
            if(data.predicted_return > 0)
            {
                alertBox.className = 'alert alert-success';
            } else if(data.predicted_return <= 0){
                alertBox.className = 'alert alert-warning';
            }
            resultData.innerHTML = `
                <p><strong>Successfully invested in ${numStocks} share(s) of ${ticker} at $${curPrice} each, for a total of ${numStocks * curPrice}.</strong></p>
            `;
        }
    })
    .catch(error => {
        alertBox.className = 'alert alert-danger';
        resultData.innerHTML = 'An error occured. Please try again.';
        console.error('Error:', error);
    });
}

function updateChart(data) {
    const wrapper = document.getElementById('chartWrapper');
    wrapper.style.display = 'block';

    const ctx = document.getElementById('stockChart').getContext('2d');
    
    if (stockChart) {
        stockChart.destroy();
    }

    const history = data.history;
    const predictedPrice = data.predicted_price;
    const currentPrice = data.current_price;
    
    // Label the days
    const labels = history.map((_, i) => `Day ${i}`);
    for (let i = 1; i <= 30; i++) {
        labels.push(i === 30 ? "30-Day Forecast" : "");
    }

    const predictionData = new Array(history.length - 1).fill(null);
    
    predictionData.push(currentPrice); 
    
    // Pad with 29 nulls to represent the 29 days of "waiting"
    for (let i = 0; i < 29; i++) {
        predictionData.push(null);
    }
    
    predictionData.push(predictedPrice);

    // Color logic
    const isIncrease = predictedPrice >= currentPrice;
    const predictionColor = isIncrease ? '#198754' : '#dc3545';

    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: history,
                    borderColor: '#3b82f6',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: '30-Day Prediction',
                    data: predictionData,
                    borderColor: predictionColor,
                    borderDash: [5, 5],
                    borderWidth: 2,
                    pointRadius: (ctx) => (ctx.dataIndex === predictionData.length - 1 ? 6 : 0), // Only show dot on the last day
                    pointBackgroundColor: predictionColor,
                    spanGaps: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: true,
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true
                    }
                },
                y: { beginAtZero: false }
            }
        }
    });
}