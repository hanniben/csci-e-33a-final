import json
import random

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Game


def index(request):
    # Filter unfinished games by player
    games = Game.objects.filter(player__username=request.user).filter(timestamp_won__isnull=True)

    # Check if any unfinished games exist for user
    if games != '':
        games = games.order_by("-timestamp_save").all()

    # Check if any finished games exist
    won_games = Game.objects.filter(timestamp_won__isnull=False)
    if won_games != '':
        won_games = won_games.order_by("-timestamp_save").all()

    # Return index page
    return render(request, "game/index.html", {
        "games":games,
        "won":won_games
    })


# Generate a new game
def new_game(request):
    if request.method == "POST":

        # Get easy or hard mode
        mode = request.POST["mode"]

        # Set grid_type as empty list
        grid_type=[]

        # Loop for 10 rows
        for x in range(10):
            
            # Create array of 10 for each grid row
            row_type = [0] * 10
            
            # If first row, set first space to visited type 3
            if x == 0:
                row_type[0] = 3

            # Add hole squares as type 1
            # Easy mode add holes in rows 2, 4, 6, and 8
            if mode == "True":
                if x in [2,4,6,8]:
                    row_type[random.randint(0,9)] = 1

            # Hard mode add holes in rows 1 through 8
            else:
                if x in [1,2,3,4,5,6,7,8]:
                    row_type[random.randint(0,9)] = 1

            # Add key squares as type 2
            while True:
                # If last row, random key placement between 0 and 8 to make sure key is not in last square
                if x == 9:
                    y = random.randint(0,8)

                # Else random key placement between 0 and 9
                else:
                    y = random.randint(0,9)

                # Add key if square is empty, repeat while loop if not
                if row_type[y] == 0:
                    row_type[y] = 2
                    break

            # Append all row types
            grid_type.extend(row_type)

        # Save game
        new_game = Game(
            player = request.user,
            squares = "".join(list(map(str,grid_type))),
            mode = bool(mode == "True")
            )
        new_game.save()

        # Redirect to game page
        return HttpResponseRedirect(reverse('game_view', args=(new_game.id,)))
        
    # If no POST return to index page
    else:
        return HttpResponseRedirect(reverse('index'))


# Display game grid
def game_view(request, id):
    # Get game by id and player
    if request.user.is_authenticated and (Game.objects.filter(pk=id, player=request.user)):
        game = Game.objects.get(pk=id)
        # Render game
        return render(request, "game/game.html", {
            "game":game
        })
    
    # Else redirect to index
    else:
        return HttpResponseRedirect(reverse('index'))


# Player move request
def move(request, id):
    # Error check PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    else:
        # Get current game object
        game = Game.objects.get(pk=id)

        # Load JSON data
        data = json.loads(request.body)
        index = data.get("squareId", "")
        type_ = data.get("type", "")

        # Convert game square types and keys to lists
        type_list = list(game.squares)
        key_list = list(game.keys)

        # If player moved into hole square
        if type_ == 1 or type_ == 4:
            # Update position to square 1 and update type
            game.position = 1
            type_list[index - 1] = 4

        else:
            # Update position to selected square and update square type
            game.position = index
            type_list[index - 1] = 3

            # If player moved into key square
            if type_ == 2:
                # Integer divide to find row and update key list
                key = (index - 1) // 10
                key_list[key] = 1

                # Convert key list back to string
                game.keys = "".join(list(map(str,key_list)))

        # Check if game is won and update timestamp
        if index == 100 and game.keys == "1111111111":
            game.timestamp_won = timezone.now()

        # Convert squares list back to string
        game.squares = "".join(list(map(str,type_list)))

        # Save game
        game.timestamp_save = timezone.now()
        game.save()

    # Return new position data
    return JsonResponse({"position": game.position, "type":game.squares[index-1], "keys":game.keys, "won":game.timestamp_won}, safe=False)


# Login a user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "game/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "game/login.html")


# Logout a user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "game/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "game/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "game/register.html")
