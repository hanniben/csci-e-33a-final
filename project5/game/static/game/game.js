document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('#game-view')) {
        token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

   // Show game view
    document.querySelector('#game-view').style.display = 'block';
    const gridId = document.querySelector('.grid-game').dataset.gameId
    let gameWon = document.querySelector('#game-view').dataset.won


    document.querySelectorAll('.grid-item button').forEach(button => {
        button.addEventListener('click', function() {
            // Get previous position
            let position = parseInt(document.querySelector('#game-view').dataset.position)

            // Get above square if any
            let above, below, left, right = 0
            if (position >= 11) {
                above = position - 10
            }
            // Get bottom square if any
            if (position <= 90) {
                below = position + 10
            }
            // Get left square if any
            if (position%10 != 1) {
                left = position - 1
            }
            // Get right square if any
            if (position%10 != 0) {
                right = position + 1
            }

            if([above, below, left, right].includes(parseInt(this.parentNode.dataset.square)) && (gameWon == 'None')) {
                const moveType = parseInt(this.parentNode.classList[1].charAt(6))
                fetch(`/move/${gridId}`, {
                    method:'PUT',
                    headers:{"X-CSRFToken":token},
                    body: JSON.stringify({
                        squareId: parseInt(this.parentNode.dataset.square),
                        type: moveType
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if ([1, 4].includes(moveType)) {
                        alert('There is a hole in the floor! You fell through and have to start from the beginning.')
                    }
                    if (moveType == 2) {
                        alert('You found a key!')
                        document.querySelectorAll('.grid-keys div.grid-item').forEach(key => {
                            if (data.keys.charAt(key.dataset.key-1) == 1) {
                                document.querySelector('[data-key="' + key.dataset.key + '"] svg').style.fill = 'red'
                            }
                        })    
                    }

                    if (data.won != null) {
                        alert('You won the game!')
                        gameWon = data.won
                        console.log(gameWon)
                    }

                    // Remove player icon from previous position
                    document.querySelector('[data-square="' + position + '"] button').removeAttribute('id')
                    // Add player icon to new position
                    document.querySelector('[data-square="' + data.position + '"] button').setAttribute('id', 'player-icon')

                    // Update position in HTML
                    document.querySelector('#game-view').dataset.position = data.position
                    // Remove square class
                    this.parentNode.classList.remove(this.parentNode.classList[1])
                    // Update square class
                    this.parentNode.classList.add('square' + data.type)
                });
            }
        })
    })




})