let pay_btn = document.getElementById('pay')
let client_secret = pay_btn.getAttribute('client_secret')
let errors = document.getElementById('card-errors')

let _firstname = document.getElementById('id_firstname').value
let _lastname = document.getElementById('id_lastname').value
let _email = document.getElementById('id_email').value
let _phone = document.getElementById('id_phone').value
let _country = document.getElementById('id_country').value

let stripe = Stripe(PUB_KEY)
let elements = stripe.elements({clientSecret: client_secret})
let card = elements.create('card')


card.mount('#card-element')
card.on(
    'change',
    (e) => {
        if( e.error ){

            errors.textContent = e.error.message
            errors.classList.add('alert')
            errors.classList.add('alert-danger')

        }else{

            errors.textContent = ''
            errors.classList.remove('alert')
            errors.classList.remove('alert-danger')
        }
    }
)

pay_function = () => {

    pay_btn.textContent = ''
    pay_btn.innerHTML = '<div class="spinner-border" role="status"></div>'

    stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: SUCCESS_URL,
          payment_method_data: {
            billing_details: {
              name: _firstname + ' ' + _lastname,
              email: _email,
              phone: _phone,
              address: {
                country: _country,
              }
            }
          },
        },
      }).then(
        (res) => {

            if(res.error){

            errors.textContent = e.error.message
            errors.classList.add('alert')
            errors.classList.add('alert-danger')
            }else{

                if(res.paymentIntent.status == 'succeeded'){

                    window.location.replace(SUCCESS_URL)
                }
            }
        }
    )
}