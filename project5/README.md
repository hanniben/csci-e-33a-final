# Untitled Dungeon Crawler Game
#### _Created by: Ashleigh Kenworthy_

Untitled Dungeon Crawler Game is a one-level game comprised of a user-manipulative grid.

## How to Play

- **Log in** to the game
- From the main page, select **Easy Mode** or **Hard Mode** and **Start** to start a new game. If you have any saved games, they will appear below. Click on a saved game to return to your last saved spot.
- You will be directed to the game page where you can move your character around the grid.
- You can move your character **one** space at a time in the **up, down, left, or right** direction.
- As you move across the grid, you will find keys. Find all 10 keys and reach the final space, marked **end here**, to finish the game.
- You will also find holes that will set you back to the beginning space.
- Your progress saves automatically, select **Main Menu** at the top of the screen to return to the main page.
- If you are signed in as a superuser, you will see a **Cheat** button at the top of the page. Selecting this button toggles the cheat view. Unvisited key squares will be outlined in blue and hole squares will be outlined in red.
- When you have finished the game, return to the main page by selecting **Main Menu** at the top of the screen.

## Files

**Project5**
- **game**
    - **static/game**
        - `game.js`:
            This file contains the front-end program that handles the user's interaction with the game. First, the JavaScript queries the id of the game and won timestamp if there is any. The button for each square is then monitored for any clicks from the user. When a button is clicked, the user's current position is queried. Once the position is read, the index of the top, bottom, left, and right adjacent squares are calculated. If the index of the button that was clicked matches one of the adjacent squares, and the game has not yet been won, a PUT request is sent to the move function in `views.py`. The move function looks at the type of the square that was selected and evaluates the user's new position. The function then passes status information back to the JavaScript.
            The JavaScript then removes the player icon from the previous square. If a key was found, the key animation plays in the selected square and the statuses at the top of the page are updated. If a hole was found, the hole animation plays in the selected square. These animation classes are removed when they finish so they can be played again for the next key or hole.
            The won timestamp of the game is read back from `views.py`. If the timestamp has been populated, the "won" player icon is updated and further movement is blocked. If the game has not been won, the selected square is updated with the player icon.
            The position dataset inside the HTML is updated with the position read back from `views.py`. The selected square's classes are then refreshed with the updated type.
            The JavaScript will continue monitoring for future user clicks.
            **cheat** function toggles red borders around unvisited hole squares, and blue borders around unvisited key squares. This function can only be used by the superuser.
        - `styles.css`:
            This file contains all the styling for the app. There are animations for finding keys and holes. Some horizontal sizing changes depending on the width of the screen.
            The game is styled as a 10 by 10 grid. I chose a grid for the ease of implementation and it allows for all squares, regardless of type, to be rendered with the same code.
    - **templates/game**
        - `game.html`: 
            At the top of this file is the game navigation. There is a button to being the user back to the main menu, and another to display a cheat overlay. The cheat overlay is only available to the superuser.
            Next is the game grid. The game django object is passed from the `game_view` function in `views.py`. This page stores the current player position and won timestamp in independent data sets. The key statuses are shown as a 1x10 grid. The default status color is grey, and found color is red. When the game page loads, the html loops through each key for a total of 10 times. The current status of the key is read, and the fill color is updated accordingly.
            The game is shown as a 10x10 grid. The html loops through each game square to create a div for a total of 100 times. Each square is given a class that corresponds to its type: whether it be a normal square, key, hole, and visited or not. This class renders the correct syle for that particular square. Each square is also given an index that is stored in the data set. The index is generated by the for loop count and will have a value between 1 and 100.
            Inside the square is a button. The button is the same size of the square and is used for player movement, position, and animations. My intention was to keep the more static styles in the square div, and update the button styles with the player's movements.
        - `index.html`:
            This file allows a logged in user to start a new game or continue a previously saved unfinished game. This page displays two radio buttons for the user to select an easy or hard mode when starting a new game.
            Below these radio buttons are selections for all unfinished games by the current user and any games that have been won by all users. The `index` function in `views.py` passes two sets of lists to this page. One list for all unfinished games, and another for all finished games. The html first loops through all unfinished games, displaying the last saved time, keys found, and difficulty mode. The data for each unfinished game is displayed as a link. The links are displayed in a scrollable table.
            The html then loops through all the finished games and displays them in a scrollable table.
        - `layout.html`:
            This file displays the title and login/logout/register selections.
        - `login.html`:
            This file displays the sign in form for a registered user to enter their username and password. If the user is not registered, they can select **Register** to be redirected to the registration page.
        - `register.html`:
            This file displays the registration form for a user to sign up for an account with their username, emai, and password. If the user is already registered, they can select **Log In here** to be redirected to the Login page.
    - `admin.py`:
        This file has two registered models: User and Game. These models can be manipulated in the Django admin pages.
    -  `apps.py`:
        This file configures the app name as **game**.
    - `models.py`:
        This file contains the two Django models: User and Game. The User model contains the users' credentials.
        The Game model contains all the information for a single game.
        **player** contains the user that is playing the game. 
        **timestamp_save** contains the date and time that the game was last saved. 
        **timestamp_won** contains the date and time that the game was finished. 
        **position** contains the user's current position as an integer value between 1 and 100. 
        **squares** contains a string of 100 characters that holds the status of each square in the game grid. Each square can have a status of: **0** for not visited empty square, **1** for not visited hole square, **2** for not visited key square, **3** for visited empty square, and **4** for visited hole square. These statuses are used to generate the correct style for each square and to generate the correct responses to user movements.
        **keys** contains a string of 10 characters that holds the status of each key. Each key can have a status of **0** for not found, and **1** for found. These statuses are used to finish the game. When all key statuses are **1** and the last space is reached, the game is won.
    - `tests.py`:
        This file contains all the tests for the app. The tests verify the functionality of the `new_game function` in `views.py`.
    - urls.py:
        This file contains all the url paths for the app.
        **index** calls the `index` function in `views.py` to render the main page.
        **login** calls the `login_view` function in `views.py` to render the login page.
        **logout** calls the `logout_view` function in `views.py` to render the logout page.
        **register** calls the `register` function in `views.py` to render the registration page.
        **new** calls the `new_game` function in `views.py` to create a new Game object.
        **game_view** calls the `game_view` function in `views.py`. The function takes in a Game object id as an integer value and renders the game page for the specific Game object.
        **move** calls the `move` function in `views.py`. The function takes in a Game object id as an integer value and gets the object data for the game. The function receives the user's position information from JavaScript and sends back the appropriate response for the game.
    - `views.py`:
        This file contains all the python functions for page rendering and Django object handling.
        **index** function generates two lists for displaying game data on the main page. The first list contains all the current user's unfinished games and orders them by the last saved timestamp. The second list contains all finished games by all users and orders them by the timestamp of when they were finished. The function returns the `index.html` template and passes these two lists to be rendered in the html.
        **new_game** creates a new Game object. The function expects to be called during a POST request. If this function is called without a POST request, the user will be redirected to the main page. During a POST request, the function takes in the mode from the request with **True** being easy mode and **False** being hard mode.
        The function creates an empty list called **grid_type**. This list will contain all 100 statuses for the grid squares. The following code loops 10 times, once for each row. In each loop, an all-zero array of length 10 is created. The first value of the first array is given a status of **3**(visited empty square). Depending on which row is being generated and what difficulty level was selected, statuses of **1**(hole square) and **2**(key square) are randomly entered into the rows. For easy difficulty, rows 2, 4, 6, and 8 (row index is base 0) will each have 1 hole square. For hard difficulty, rows 1 thorugh 8 will each have 1 hole square. All rows in both difficulties each have 1 key, for a total of 10 keys for every game. The logic for setting a key square is in a while loop. In the event that the randomly selected square has already been assinged as a hole, the logic will run again until an empty square is selected and set that as a key.
        Once all 10 rows have been generated, they are packed together into a string and saved to a new Game object with the current user as the player. The logic then redirects to the **game_view** function to render the game for the user.
        **game_view** function takes in the game id as an integer value and gets the corresponding Game object. The function then renders the `game.html` template and passes the object to the html. This function error checks to make sure that the correct user is trying to access the game. If an incorrect user tries to access the game, they will be redirected to the main page.
        **move** gets the user's request to move their character. The function expects to be called during a PUT request. If this function is called without a PUT request, an error is returned in a Json Response. During a PUT request, the function takes in the game id from the `move/<int:id>` url. From a JavaScript fetch, the function takes in the index and type of the square that the user is moving to. If the type is **1**(unvisited hole square) or **4**(visited hole square), the user's new position is set back to the beginning. Else, the user's position is updated to the square they selected. If the type is **2**(unvisited key square) the row number is derived from the index and the approrpiate key status is updated.
        The function then checks if the game has been won: if space 100 has been reached and all keys have been found. If the game has been won, the **timestamp_won** is updated.
        The game object is then updated with position, square status, key status, save time stamp, and won timestamp. A Json response is returned with the current postition, updated type of user selected square, key status, and won timestamp.
