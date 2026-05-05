# StockUp

StockUp is a competitive social and financial platform that merges fantasy football with real-world stock market data. Users can team up, invest their money, and compete to
create the most profitable portfolio on the leaderboard.

## Features

* Stock price predictor
* Creation, joining, leaving, and deletion of teams
* Buying and selling stocks
* Leaderboard for top teams
* User portfolio page
* Admin interface

## Setup

### Prerequisites

* Python 3.x
* Pip

### Configuration

1. Download and install [Python](https://www.python.org/downloads/) if you haven't already.
2. Download or clone this repo `git clone https://github.com/mdcrapse/stock`
3. Go into the folder for the downloaded repo
4. Create a virtual environment: `python -m venv .venv`
5. Activate virtual environment: `.\\.venv\\Scripts\\activate.bat` (windows), `source .venv/bin/activate` (Linux)
6. Install requirements: `pip install -r requirements.txt`
7. Apply database migrations: `python manage.py migrate`
8. Create a superuser: `python manage.py createsuperuser`

## Usage

### Run the site
To use the site:

1. Run server: `python manage.py runserver`
2. Go to `127.0.0.1:8000`
3. Either sign in with existing credentials or create a new account to use the app

### Updating the Database
If you need to update the structure of the database:

1. Modify `./stocks/models.py`.
2. Make migrations: `python manage.py makemigrations stocks`
3. Apply migrations: `python manage.py migrate`

### View/Modify Database
To view the database from the admin page:

1. Ensure the desired model is in `./stocks/admin.py`
2. Run server: `python manage.py runserver`
3. Open `127.0.0.1/admin/` page.

## Tech Stack

### Backend
* Python
* Django

### Database
* SQLite

### Frontend
* Django Templating
* HTML
* CSS
* JS
* Bootstrap

### Packages used
* yfinance
* Django
* XGBoost