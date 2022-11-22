let all = document.getElementById('all');
let paid = document.getElementById('paid');
let topay = document.getElementById('topay');

all.addEventListener('click', ()=>{
    
    // chage ui
    all.classList.add('border-dark', 'border-3')
    paid.classList.remove('border-dark', 'border-3')
    topay.classList.remove('border-dark', 'border-3')
})

paid.addEventListener('click', () => {

    all.classList.remove('border-dark', 'border-3')
    paid.classList.add('border-dark', 'border-3')
    topay.classList.remove('border-dark', 'border-3')
})

topay.addEventListener('click', () => {

    all.classList.remove('border-dark', 'border-3')
    paid.classList.remove('border-dark', 'border-3')
    topay.classList.add('border-dark', 'border-3')
})