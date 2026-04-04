from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .predictor import predict_stock
import json
from django.http import JsonResponse
from .forms import SignUpForm, SignInForm

def index(request):
    latest_question_list = [] # Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "stocks/index.html", context)


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def invest(request):
    if request.method == "POST":
            # Check if the request is JSON
            data = json.loads(request.body)
            ticker = data.get('ticker_symbol')
            sector = data.get('sector')
            result = predict_stock(ticker, sector)
            
            return JsonResponse(result)

    return render(request, "invest.html")

def login_view(request):
    form = SignInForm(request, data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    form = SignUpForm(data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def teams(request):
    if(request.method == 'POST'):
        pass

    return render(request, "teams.html")

def leaderboard(request):
    if(request.method == 'POST'):
        pass

    return render(request, "leaderboard.html")

def teamview(request):
    if(request.method == 'POST'):
        pass

    return render(request, "teamview.html")
