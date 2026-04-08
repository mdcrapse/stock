from django.urls import path

from . import views

urlpatterns = [
    # Main pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("invest/", views.invest, name="invest"),
    path("portfolio/<str:username>/", views.portfolio, name="portfolio"),

    # User auth pages
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path('logout/', views.logout_view, name='logout'),

    # Team pages
    path("teams/", views.teams, name="teams"),
    path("teams/add", views.add_team, name="addteam"),
    path("teams/delete/<str:team_name>", views.delete_team, name="deleteteam"),
    path("teamview/join/<str:team_name>", views.join_team, name="jointeam"),
    path("teamview/leave/<str:team_name>", views.leave_team, name="leaveteam"),
    path("teamview/<str:team_name>/", views.teamview, name="teamview"),

    # Investment pages
    path("user/get_balance/", views.getUserBalance, name="getuserbalance"),
    path("user/invest/", views.investInStock, name="investinstock"),
]
