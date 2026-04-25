// Auto fills the ticker_symbol based on what is in the table row
document.addEventListener('click', function (event) {
    // Check that the click is correct
    const isModal = event.target.classList.contains('btn-modal');
    if (!isModal) return;

    // Get the row and ticker symbol from the row
    const row = event.target.closest('tr');
    const ticker_symbol = row.querySelector('.ticker').innerHTML;

    // Get the field and set the value
    ticker_field = document.getElementById("ticker");
    ticker_field.value = ticker_symbol;
});