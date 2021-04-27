document.addEventListener('DOMContentLoaded', function() {

    token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

   // Show game view
    document.querySelector('#game-view').style.display = 'block';
    const gridId = document.querySelector('.grid-container').dataset.gameId


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

            if([above, below, left, right].includes(parseInt(this.parentNode.dataset.square))) {
                fetch(`/move/${gridId}`, {
                    method:'PUT',
                    headers:{"X-CSRFToken":token},
                    body: JSON.stringify({
                        squareId: parseInt(this.parentNode.dataset.square),
                        type: parseInt(this.parentNode.classList[1].charAt(6))
                    })
                })
                .then(response => response.json())
                .then(data => {
                    document.querySelector('[data-square="' + position + '"] button').innerHTML = ''
                    document.querySelector('[data-square="' + data.position + '"] button').innerHTML = '<img id="player-icon">'

                    // update position
                    document.querySelector('#game-view').dataset.position = data.position
                    this.parentNode.classList.remove(this.parentNode.classList[1])
                    this.parentNode.classList.add('square' + data.type)
                });
            }
        })
    })




})