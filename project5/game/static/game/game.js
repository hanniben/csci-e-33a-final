document.addEventListener('DOMContentLoaded', function() {
    // CSRF token
    const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Show game view
    const gridId = document.querySelector('.grid-game').dataset.gameId;
    let gameWon = document.querySelector('.grid-game').dataset.won;

    // Get all square buttons
    document.querySelectorAll('.grid-item button').forEach(button => {
        button.addEventListener('click', function() {
            // Get previous position
            let position = parseInt(document.querySelector('.grid-game').dataset.position);

            // Get above square if any
            let above, below, left, right = 0;
            if (position >= 11) {
                above = position - 10;
            }
            // Get bottom square if any
            if (position <= 90) {
                below = position + 10;
            }
            // Get left square if any
            if (position%10 != 1) {
                left = position - 1;
            }
            // Get right square if any
            if (position%10 != 0) {
                right = position + 1;
            }

            // Move player if adjacent square selected and game is not won
            if([above, below, left, right].includes(parseInt(this.parentNode.dataset.index)) && (gameWon == 'None')) {
                const moveType = parseInt(this.parentNode.classList[1].charAt(6));
                fetch(`/move/${gridId}`, {
                    method:'PUT',
                    headers:{"X-CSRFToken":token},
                    body: JSON.stringify({
                        squareId: parseInt(this.parentNode.dataset.index),
                        type: moveType
                    })
                })
                .then(response => response.json())
                .then(data => {
                    // Remove player icon from previous position
                    document.querySelector('[data-index="' + position + '"] button').removeAttribute('id');

                    // If move to hole square, start hole animation
                    if (moveType == 1 || moveType == 4) {
                        this.classList.add('hole-animation');
                    }
                    
                    // If move to key square, start key animation
                    else if (moveType == 2) {
                        this.classList.add('key-animation');
                        // Update key display at top of page to show found keys
                        document.querySelectorAll('.grid-keys div.grid-item').forEach(key => {
                            if (data.keys.charAt(key.dataset.key-1) == 1) {
                                document.querySelector('[data-key="' + key.dataset.key + '"] svg').style.fill = 'red';
                            }
                        });
                    }

                    // If game is won, change player icon and set gameWon to prevent further movement
                    if (data.won != null) {
                        document.querySelector('[data-index="' + data.position + '"] button').setAttribute('id', 'won-icon');
                        this.classList.add('won-animation');
                        gameWon = data.won;
                    }

                    // Add player icon to new position
                    else {
                        document.querySelector('[data-index="' + data.position + '"] button').setAttribute('id', 'player-icon');
                    }

                    // Update position in HTML
                    document.querySelector('.grid-game').dataset.position = data.position;
                    // Remove all classes
                    this.parentNode.className = '';
                    // Update square class
                    this.parentNode.classList.add('grid-item', 'square' + data.type);

                    // Remove animation classes when dont
                    this.addEventListener('animationend', () => {
                        this.classList.remove('key-animation');
                        this.classList.remove('hole-animation');
                        this.classList.remove('won-animation');
                    });
                });
            }
        });
    });
});


// Display cheats
function cheat() {
        // Outline squares with holes in red
        document.querySelectorAll(".square1").forEach(hole => {
            hole.classList.toggle("hole-cheat");
        });

        // Outline squares with keys in blue
        document.querySelectorAll(".square2").forEach(key => {
            key.classList.toggle("key-cheat");
        });
}
