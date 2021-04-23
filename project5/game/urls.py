
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_game, name="new"),
    path("game/<int:id>", views.game_view, name="game_view"),
    path("move/<int:id>", views.move, name="move")
]
