let btns = document.querySelectorAll('button');



for (let btn of btns) {
    btn.addEventListener('click', () => {
        if (btn.classList.value == 'id_password') {
            let pass = document.querySelector(`input[id=${btn.classList.value}]`);
            if (btn.firstChild.style.filter == 'invert(50%)') {
                btn.firstChild.style.filter = 'invert(0)';
                pass.type = 'text';
            } else {
                btn.firstChild.style.filter = 'invert(50%)';
                pass.type = 'password';
            }
        } else {
            let pass = document.querySelector(`input[id=${btn.classList.value}]`);
            if (btn.firstChild.style.filter == 'invert(50%)') {
                btn.firstChild.style.filter = 'invert(0)';
                pass.type = 'text';
            } else {
                btn.firstChild.style.filter = 'invert(50%)';
                pass.type = 'password';
            }
        }
    })
}


