from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .predictor import predict_stock
import json
from django.http import JsonResponse

# from .models import Question


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


def detail(request, question_id):
    question = None # get_object_or_404(Question, pk=question_id)
    return render(request, "stocks/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
