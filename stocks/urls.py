from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("invest/", views.invest, name="invest"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("teams/", views.teams, name="teams"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("teamview/", views.teamview, name="teamview"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
