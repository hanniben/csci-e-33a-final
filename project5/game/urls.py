from django.urls import path

from . import views

urlpatterns = [
    # Main page
    path("", views.index, name="index"),
    # Login
    path("login", views.login_view, name="login"),
    # Logout
    path("logout", views.logout_view, name="logout"),
    # Register
    path("register", views.register, name="register"),
    # Generate a new game
    path("new", views.new_game, name="new"),
    # Display game
    path("game/<int:id>", views.game_view, name="game_view"),
    # Move a square
    path("move/<int:id>", views.move, name="move")
]
