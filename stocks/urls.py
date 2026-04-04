from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("invest/", views.invest, name="invest"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path("teams/", views.teams, name="teams"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("teamview/<str:team_name>/", views.teamview, name="teamview"),
    path("user/get_balance/", views.getUserBalance, name="getuserbalance"),
    path("user/invest/", views.investInStock, name="investinstock"),
]
