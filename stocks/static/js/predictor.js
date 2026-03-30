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
            `;
        }
    })
    .catch(error => {
        alertBox.className = 'alert alert-danger';
        resultData.innerHTML = 'An error occured. Please try again.';
        console.error('Error:', error);
    });
});