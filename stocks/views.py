from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Sum, Avg
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .predictor import predict_stock
from .forms import SignUpForm, SignInForm
from .models import Team, Member, Transaction, TransactionHistory, Owns, User, Stock

import json
import datetime

def index(request: HttpRequest) -> HttpResponse:
    latest_question_list = [] # Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "stocks/index.html", context)


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "contact.html")

@login_required()
def invest(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
            # Check if the request is JSON
            data = json.loads(request.body)
            ticker = data.get('ticker_symbol')
            sector = data.get('sector')
            result = predict_stock(ticker, sector)
            
            return JsonResponse(result)

    return render(request, "invest.html")

def login_view(request: HttpRequest) -> HttpResponse:
    form = SignInForm(request, data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    return render(request, 'login.html', {'form': form})

def signup_view(request: HttpRequest) -> HttpResponse:
    form = SignUpForm(data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html', {'form': form})

@login_required()
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

@login_required()
def teams(request: HttpRequest) -> HttpResponse:
    teams = []
    if(request.method == 'POST'):
        search = request.POST.get('search')
        teams = Team.objects.filter(team_name__icontains=search).order_by('-balance_per_capita')
    else:
        teams = Team.objects.order_by('-balance_per_capita')[:10]

    view_teams = []
    for t in teams:
        view_teams.append({
            'team_name': t.team_name,
            'num_members': Member.objects.filter(team=t).count(),
            'balance_per_capita': t.balance_per_capita,
        })
    
    return render(request, "teams.html", {'teams': view_teams})

@login_required()
def teamview(request: HttpRequest, team_name: str) -> HttpResponse:
    team = get_object_or_404(Team, team_name__iexact=team_name)
    members = Member.objects.filter(team=team)
    names = list(members.values_list('user__username', flat=True))
    total_balance = (members.aggregate(total=Sum('user__balance'))['total'] or 0) / 100.0
    team.balance_per_capita = 0
    if(members.count() > 0):
        team.balance_per_capita = total_balance / (members.count())

    team.save()

    user_is_on_team = False
    if(Member.objects.filter(user=request.user, team=Team.objects.filter(team_name=team_name)[0])):
        user_is_on_team = True

    user_owns_team = False
    if(Team.objects.filter(owner=request.user, team_name=team_name)):
        user_owns_team = True

    print(user_owns_team)

    return render(request, "teamview.html", {
        'team_name': team.team_name,
        'num_members': members.count(),
        'member_names': names,
        'balance_per_capita': team.balance_per_capita,
        'total_balance': total_balance,
        'user_is_on_team': user_is_on_team,
        'user_owns_team': user_owns_team,
    })

@login_required()
def leaderboard(request: HttpRequest) -> HttpResponse:
    mean_bpc = 0
    if(Team.objects.count() > 0):
        mean_bpc = Team.objects.aggregate(Avg('balance_per_capita')).get('balance_per_capita__avg')
    
    teams = Team.objects.filter(balance_per_capita__gte=mean_bpc)

    return render(request, 'leaderboard.html', {'teams': teams})

@login_required()
@require_http_methods(['POST'])
def join_team(request: HttpRequest, team_name: str) -> HttpResponse:
    new_member = Member(
        user = request.user,
        team = Team.objects.filter(team_name=team_name).first()
    )

    new_member.save()
    return redirect('teamview', team_name=team_name)

@login_required()
@require_http_methods(['POST'])
def leave_team(request: HttpRequest, team_name: str) -> HttpResponse:
    member = Member.objects.filter(user=request.user, team=Team.objects.filter(team_name=team_name).first()).first()
    member.delete()
    return redirect('teamview', team_name=team_name)

@login_required()
@require_http_methods(['POST'])
def add_team(request: HttpResponse) -> HttpResponse:
    data = request.POST
    team_name = data.get("team_name")

    # Check that the team doesn't already exist
    if Team.objects.filter(team_name=team_name).exists():
        messages.error(request, f"Error: Team {team_name} already exists.")

    # If not, create a new team
    else:
        new_team = Team(
            team_name=team_name,
            creation_date=datetime.datetime.now(),
            balance_per_capita=0,
            owner=request.user,
        )
        new_team.save()
        messages.success(request, "Team added successfully!")

    return redirect('teams')

@login_required()
@require_http_methods(['POST'])
def delete_team(request: HttpResponse, team_name: str) -> HttpResponse:
    team = Team.objects.filter(owner=request.user, team_name=team_name).first()

    if(team):
        team.delete()
        messages.success(request, "Team deleted successfully!")

    else:
        messages.success(request, "Error: Try again")

    return redirect('teams')

@login_required()
def portfolio(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username__iexact=username)
    stocks = Stock.objects.filter(owns__user=user)
    transactions = Transaction.objects.filter(transactionhistory__user=user).order_by('-date')
    teams = Member.objects.filter(user=user)
    team_names = teams.values_list('team__team_name', flat=True)

    payed = abs(stocks.aggregate(total=Sum('value'))['total'] or 0)
    tickers = list(stocks.values_list('ticker', 'shares'))
    stock_prices = _current_stock_price(tickers)
    current_share_price = sum(stock_prices.values())
    pay_diff = current_share_price - payed

    stocks_formatted = stocks.values('ticker', 'value', 'shares')
    for s in stocks_formatted:
        s['actual_value'] = stock_prices[s['ticker']]
        s['value_diff'] = f'{s['actual_value'] - s['value']:.2f}'
        s['actual_value'] = f'{s['actual_value']:.2f}'

    return render(request, "portfolio.html", {
        'username': user.username,
        'balance': user.balance / 100.0,
        'num_stocks': stocks.count(),
        'num_shares': stocks.aggregate(total=Sum('shares'))['total'] or 0,
        'total_stock_value': f'{current_share_price:.2f}',
        'total_stock_purchase_value': f'{payed:.2f}',
        'total_value_earned': f'{pay_diff:.2f}',
        'team_names': team_names,
        'stocks': stocks_formatted,
        'transactions': transactions,
    })

@login_required()
@require_http_methods(["GET"])
def getUserBalance(request: HttpRequest) -> JsonResponse:
    username = request.user.username

    # Account for the user balance being cents
    user_balance = (request.user.balance / 100)

    return JsonResponse({'username': username, 'balance': user_balance})

@login_required()
@require_http_methods(["POST"])
def investInStock(request: HttpRequest) -> JsonResponse:
    # Get the data from the POST
    try:
        data = json.loads(request.body)
        
        # Access the keys
        ticker_symbol = data.get("symbol")
        shares = data.get("amount")
        total_price = data.get("total_price")

        if(not ticker_symbol or not shares or not total_price):
            return JsonResponse({'error': 'Something went wrong'}, status=400)

        # Create a new transaction
        new_transaction = Transaction(
            ticker=ticker_symbol,
            date=datetime.datetime.now(),
            shares=shares
        )
        new_transaction.save()
        
        # Create new transaction history entry
        new_t_history = TransactionHistory(
            user=request.user,
            transaction=new_transaction
        )
        new_t_history.save()

        # Create / modify an owns entry
        user_portfolio = Owns.objects.filter(user=request.user).select_related('stock')

        # Search through portfolio to find if they already have this stock
        found_stock = False
        for entry in user_portfolio:
            if(entry.stock.ticker == ticker_symbol):
                found_stock = True
                entry.stock.shares += int(shares)
                entry.stock.save()
                break

        if(found_stock == False):
            # If they dont have the stock, create a new stock entry
            new_stock = Stock(
                shares=shares,
                ticker=ticker_symbol,
                value=total_price
            )
            new_stock.save()

            # Create a new entry in owns
            new_owns = Owns(
                user=request.user,
                stock=new_stock
            )
            new_owns.save()

        # Take away that shares of money from the user
        request.user.balance -= (total_price * 100) # multiply to account for dollars -> cents
        request.user.save()

        return JsonResponse({'status': 'success', 'message': 'Investment processed'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Something went wrong'}, status=400)

    # Return success message
    return JsonResponse({'Success': 200})

# Returns the single share price of the specified tickers.
def _current_stock_price(tickers: list[tuple[str, int]]) -> dict[str, float]:
    import yfinance as yf
    ticker = yf.Tickers(" ".join([t for (t, _) in tickers])).tickers
    return {t: ticker[t].history(period='1d')['Close'].iloc[0] * s for (t, s) in tickers}
