var select_buttons = document.querySelectorAll('.select-button');
var confirm_buttons = document.querySelectorAll('.confirm-button')

// controll the user to select just one movie
var selected = false;

function showSelectedMovie(card, select_btn, unselect_btn) {
    // this is where the card will go (on top)
    var SelectedMovieBlock = document.getElementById('selected-movie');
    // this is where the card comes from
    var OriginBlock = select_btn.parentElement.parentElement.parentElement;

    var confirmButton = card.querySelector(".confirm-button");
    confirmButton.style.display = 'inline-block';

    SelectedMovieBlock.appendChild(card);

   
    unselect_btn.addEventListener('click', function() {
        // return card to its original block
        OriginBlock.appendChild(card)
        select_btn.style.display = 'inline-block';
        unselect_btn.style.display = 'none'
        confirmButton.style.display = 'none';
        // allow user to select another movie
        selected = false;
    })
    
}

// This function takes the movie that the user chose and calls showSelectMovie to show the selected one.
function getCard(select_btn) {
    select_btn.addEventListener('click', function() {
        var card = select_btn.parentElement.parentElement;
        var unselect_btn = card.querySelector(".unselect-button")
        if (!selected){
            selected = true;    
            select_btn.style.display = 'none'
            unselect_btn.style.display = 'inline-block'
            showSelectedMovie(card, select_btn, unselect_btn);
        }
    })
}




select_buttons.forEach(getCard)
