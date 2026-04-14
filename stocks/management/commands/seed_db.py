from django.core.management.base import BaseCommand
from django_seed import Seed
from stocks.models import User, Stock, Team, Member, StockHistory
import random

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # 1. Seed Users
        seeder.add_entity(User, 5, {
            'balance': lambda x: random.randint(100000, 1000000),
            'is_staff': False,
            'is_superuser': False,
        })

        # 2. Seed Stocks
        tickers = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT']
        seeder.add_entity(Stock, 5, {
            'ticker': lambda x: tickers.pop(),
            'shares': lambda x: random.randint(10, 500),
            'value': lambda x: random.randint(1000, 50000),
        })

        # Execute the first batch to get IDs for foreign keys
        inserted_pks = seeder.execute()
        
        self.stdout.write(self.style.SUCCESS("Users and Stocks created!"))

        # 3. Custom Logic for Teams (linking to seeded users)
        users = User.objects.all()
        for i in range(3):
            Team.objects.create(
                team_name=f"Team {i}",
                creation_date="2026-01-01",
                balance_per_capita=50000,
                owner=random.choice(users)
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))