from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from .predictor import predict_stock
import json
from .forms import SignUpForm, SignInForm
from .models import Team, Member, Transaction, TransactionHistory, Owns, User, Stock
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
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

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

def teams(request: HttpRequest) -> HttpResponse:
    if(request.method == 'POST'):
        pass

    return render(request, "teams.html")

def leaderboard(request: HttpRequest) -> HttpResponse:
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
    
    return render(request, "leaderboard.html", {'teams': view_teams})

def teamview(request: HttpRequest, team_name: str) -> HttpResponse:
    team = get_object_or_404(Team, team_name__iexact=team_name)
    members = Member.objects.filter(team=team)
    names = list(members.values_list('user__username', flat=True))
    total_balance = members.aggregate(total=Sum('user__balance'))['total'] or 0
    return render(request, "teamview.html", {
        'team_name': team.team_name,
        'num_members': members.count(),
        'member_names': names,
        'balance_per_capita': team.balance_per_capita,
        'total_balance': total_balance,
    })

@require_http_methods(["GET"])
def getUserBalance(request: HttpRequest) -> JsonResponse:
    username = request.user.username

    # Account for the user balance being cents
    user_balance = (request.user.balance / 100)

    return JsonResponse({'username': username, 'balance': user_balance})

@require_http_methods(["POST"])
def investInStock(request: HttpRequest) -> JsonResponse:
    # Get the data from the POST
    try:
        data = json.loads(request.body)
        
        # Access the keys
        ticker_symbol = data.get("symbol")
        amount = data.get("amount")
        total_price = data.get("total_price")

        # Create a new transaction
        new_transaction = Transaction(
            ticker=ticker_symbol,
            date=datetime.datetime.now(),
            amount=amount
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
                entry.stock.shares += int(amount)
                entry.stock.save()
                break

        if(found_stock == False):
            # If they dont have the stock, create a new stock entry
            new_stock = Stock(
                shares=amount,
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

        # Take away that amount of money from the user
        request.user.balance -= (total_price * 100) # multiply to account for dollars -> cents
        request.user.save()

        return JsonResponse({'status': 'success', 'message': 'Investment processed'}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Something went wrong'}, status=400)

    # Return success message
    return JsonResponse({'Success': 200})

