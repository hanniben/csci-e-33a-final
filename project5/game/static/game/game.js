document.addEventListener('DOMContentLoaded', function() {

    token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

   // Show game view
    document.querySelector('#game-view').style.display = 'block';
    const gridId = document.querySelector('.grid-container').dataset.gameId
    let position = parseInt(document.querySelector('#game-view').dataset.position)

    if (position >= 11) {
        let above = position - 10
        document.querySelector('[data-square="' + above + '"] button').addEventListener('click', function() {
            fetch(`/move/${gridId}`, {
                method:'PUT',
                headers:{"X-CSRFToken":token},
                body: JSON.stringify({
                    squareId: above,
                    type: this.parentNode.classList[1].charAt(6)
                })
            })
        })
    }

    if (position <= 90) {
        let below = position + 10
        document.querySelector('[data-square="' + below + '"] button').addEventListener('click', function() {
            fetch(`/move/${gridId}`, {
                method:'PUT',
                headers:{"X-CSRFToken":token},
                body: JSON.stringify({
                    squareId: below,
                    type: this.parentNode.classList[1].charAt(6)
                })
            })
            .then(response => response.json())
            .then(data => {
                // update position
                position = data.position
                this.parentNode.classList.remove(this.parentNode.classList[1])
                this.parentNode.classList.add('square' + data.type)
                this.innerHTML = data.type
            });
        })
    
    }

    if (position%10 != 1) {
        let left = position - 1
        document.querySelector('[data-square="' + left + '"] button').addEventListener('click', function() {
            console.log('hello')
        })
    }

    if (position%10 != 0) {
        let right = position + 1
        document.querySelector('[data-square="' + right + '"] button').addEventListener('click', function() {
            console.log('hello')
        })
    }




    document.querySelectorAll('#grid-item button')
    
    fetch(`/grid/${gridId}`, {
        method:'GET',
    })
    .then(response => response.json())
    .then(data => {
        // add liked class to change heart to red
        if (data.liked) {

            this.classList.add('liked');

        }

        // remove liked class to change heart to black

        else {

            this.classList.remove('liked');

        }

        // update like count

        this.parentNode.parentNode.querySelector('#like-count').innerHTML = data.count;

    });


    const grid = document.createElement('div')
    grid.classList.add('grid-container')

    grid.createElement



})