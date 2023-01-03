const alert = document.querySelector('.alert')
const form = document.querySelector('.token-form')
const submitBtn = document.querySelector('.submit-btn')
const pass1 = document.getElementById('pass1')
const pass2 = document.getElementById('pass2')
const pass3 = document.getElementById('pass3')
const name = document.getElementById('name')

const APP_URL = "http://127.0.0.1:8888"
// const APP_URL = "http://reluctanttycoon.com/crypto"
form.addEventListener('submit', updateAccount)

async function makeAPICall(url = '', method="POST", data = null) {
    if (data){
        data = JSON.stringify(data)
    }
    // Default options are marked with *
    const response = await fetch(APP_URL+url, {
      method: method, // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      //referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      referrerPolicy: 'strict-origin-when-cross-origin',
      body: data // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function displayAlert(text, color) {
    alert.textContent = text
    alert.classList.add(`alert-${color}`)

    setTimeout(() => {
        alert.textContent = ''
        alert.classList.remove(`alert-${color}`)
    }, 10000)
}

function updateAccount(e) {
    e.preventDefault()

    const pass_1 = pass1.value
    const pass_2 = pass2.value
    const pass_3 = pass3.value
    if (!pass_1 || !pass_2 || !pass_3){
        displayAlert('Please enter account details and try again','danger')
        setBackToDefault()
        return
    }
}

function setBackToDefault() {
    pass1.value = ''
    pass2.value = ''
    pass_3.value = ''
    name.value = ''
}
