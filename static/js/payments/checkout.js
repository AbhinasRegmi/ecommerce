const stripe = Stripe(STRIPE_PUB_KEY);

let elements;
let errors = document.getElementById('card-errors');


document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

    
elements = stripe.elements({clientSecret: CLIENT_SECRET})

address = elements.create('address', {
  mode: 'billing',
  fields: {
    phone: 'always',
  },

  defaultValues: {
    name: NAME,
    phone: PHONE,
    address: {
      line1: LINE,
      city: CITY,
      postal_code: CODE,
      country: COUNTRY,
    }
  },

  validation: {
    phone: {
      required: 'always',
    },
      }
    })

address.mount('#address-element')

const paymentElementOptions = {
  layout: "tabs",
};
  
const paymentElement = elements.create("payment", paymentElementOptions);
paymentElement.mount("#payment-element");
country.value = 'NP';
console.log(country.value)

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: "http://localhost:8000" + SUCCESS_URL,
    },
  }
  );

  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred. Try again later.");
  }

  setLoading(false);
}

function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}


function showMessage(messageText) {
  errors.textContent = messageText
  errors.classList.add('alert')
  errors.classList.add('alert-danger')
}