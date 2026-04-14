import random
import string
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from stocks.models import Stock, Team, Member, Owns, Transaction, TransactionHistory, StockHistory

User = get_user_model()

class Command(BaseCommand):
    help = "Fills the DB with a chaotic amount of random data"

    def handle(self, *args, **kwargs):
        # 1. Cleanup existing data
        self.stdout.write("Purging old data...")
        [m.objects.all().delete() for m in [Member, Owns, TransactionHistory, Transaction, Team, StockHistory, Stock, User]]

        # Helper to generate random strings
        def rand_str(length=8):
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

        # 2. Create 100 Random Users
        self.stdout.write("Generating 100 users...")
        users = []
        for _ in range(100):
            u = User.objects.create_user(
                username=f"user_{rand_str(5)}",
                password="password123",
                balance=random.randint(1000, 10000000) # cents
            )
            users.append(u)

        # 3. Create 30 Random Stocks
        self.stdout.write("Generating 30 stocks and history...")
        stocks = []
        for _ in range(30):
            ticker = "".join(random.choices(string.ascii_uppercase, k=random.randint(3, 5)))
            s = Stock.objects.create(
                ticker=ticker,
                shares=random.randint(100, 1000000),
                value=random.randint(100, 50000)
            )
            stocks.append(s)
            
            # Generate 10 days of history for each stock
            for d in range(10):
                StockHistory.objects.create(
                    day=d,
                    date=timezone.now().date(),
                    predicted_price=random.randint(100, 50000),
                    ticker=ticker
                )

        # 4. Create 15 Random Teams
        self.stdout.write("Generating 15 teams...")
        teams = []
        for _ in range(15):
            t = Team.objects.create(
                team_name=f"Team-{rand_str(4).upper()}",
                creation_date=timezone.now().date(),
                balance_per_capita=random.randint(1000, 50000),
                owner=random.choice(users)
            )
            teams.append(t)

        # 5. The Chaos: Massive Relationships
        self.stdout.write("Linking users to stocks, teams, and transactions...")
        for u in users:
            # Join 1-3 random teams
            for t in random.sample(teams, random.randint(1, 3)):
                Member.objects.create(user=u, team=t)

            # Invest in 2-6 random stocks
            for s in random.sample(stocks, random.randint(2, 6)):
                Owns.objects.create(user=u, stock=s)
                
                # Create a few random transactions for each investment
                for _ in range(random.randint(1, 3)):
                    tx = Transaction.objects.create(
                        date=timezone.now(),
                        shares=random.randint(-50, 100), # negative represents selling
                        ticker=s.ticker
                    )
                    TransactionHistory.objects.create(user=u, transaction=tx)

        self.stdout.write(self.style.SUCCESS("Database is now a beautiful mess of random data!"))