let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open')
}

function unselectCheckboxes(currentCheckboxId) {
    var checkboxes = document.querySelectorAll("input[type='checkbox']");

    checkboxes.forEach(function(checkbox) {
    if (checkbox.id !== currentCheckboxId) {
        checkbox.checked = false;
    }
    });
}
function toggleInput(checkboxId, inputId) {
    var checkbox = document.getElementById(checkboxId);
    var input = document.getElementById(inputId);
    
    if(checkboxId == "round-trip")
        input.disabled = !checkbox.checked;

    else if(checkboxId == "one-way")
        input.disabled = checkbox.checked;
  }

//Rapid API => Skyscanner
//https://rapidapi.com/3b-data-3b-data-default/api/skyscanner44/