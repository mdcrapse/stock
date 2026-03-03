# StockUp

TODO description

## Contents

TODO

### Setup

1. Create and activate a virtual environment: `python -m venv .venv`
2. Activate virtual environment: `.\\.venv\\Scripts\\activate.bat` (windows), `source .venv/bin/activate` (Linux)
2. Install requirements: `pip install -r requirements.txt`

### Update Database Models

1. Modify `./stocks/modals.py`.
2. Create migrations: `python manage.py migrate`

### View/Modify Database

1. Ensure `./stocks/admin.py` has desired model.
2. If haven't, create user: `python manage.py createsuperuser`
3. Run server: `python manage.py runserver`
4. Open `*/admin/` page.
