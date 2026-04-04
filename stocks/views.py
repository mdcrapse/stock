from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from .predictor import predict_stock
import json
from .forms import SignUpForm, SignInForm
from .models import Team, Member
from django.db.models import Sum

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
