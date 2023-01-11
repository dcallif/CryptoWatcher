const alert = document.querySelector('.alert')
const form = document.querySelector('.token-form')
const token = document.getElementById('name')
const ticker = document.getElementById('ticker')
const amountHeld = document.getElementById('amount')
const address = document.getElementById('accountAddress')
const user_email = document.getElementById('user_email')
const submitBtn = document.querySelector('.submit-btn')
const container = document.querySelector('.token-container')
const list = document.querySelector('.token-list')
const clearBtn = document.querySelector('.clear-btn')

function numberWithCommas(x) {
    return x.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

let editElement
let editFlag = false
let editID = ''
const APP_URL = "http://127.0.0.1:8888"
// const APP_URL = "http://reluctanttycoon.com/crypto"

form.addEventListener('submit', addItem)

window.addEventListener('DOMContentLoaded', setupItems)

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



function addItem(e) {
    e.preventDefault()

    const name = token.value
    const item_ticker = ticker.value
    const amount = amountHeld.value
    const user = user_email.value
    const accountAddress = address.value

    if (!name || !item_ticker || !amount || !user){
        displayAlert('Please enter crypto details','danger')
        return
    }

    if (!editFlag) {
        makeAPICall(`/token`, "POST", { "name":name, "ticker":item_ticker, "amountHeld":amount,
    "user_email":user, "accountAddress": accountAddress })
            .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
            displayAlert('Token added to the list!', 'success')
            container.classList.add('show-container')
            createListItem(data.id, item_ticker + "", amount + "", 0)
        });
    setBackToDefault()
    } else if (editFlag) {
        makeAPICall(`/token/${name}`, 'PUT', { "name":name, "ticker":item_ticker, "amountHeld":amount,
    "accountAddress": accountAddress })
            .then(data => {
                editElement.innerHTML = title
                displayAlert('Todo edited', 'success')
                setBackToDefault()
        })
    }
    location.reload()
}

function displayAlert(text, color) {
    alert.textContent = text
    alert.classList.add(`alert-${color}`)

    setTimeout(() => {
        alert.textContent = ''
        alert.classList.remove(`alert-${color}`)
    }, 10000)
}

function deleteTodo(e) {
    const user = user_email.value
    const element = e.currentTarget.parentElement.parentElement
    const id = element.getAttribute("token-name")
    makeAPICall(`/token/${id}`, "DELETE", {"user_email":user}).then((data) => {
        list.removeChild(element)
        if (list.children.length === 0) {
            container.classList.remove('show-container')
        }
        displayAlert('Token holding deleted', 'danger')
        setBackToDefault()
    })
}

function editTodo(e) {
    const element = e.currentTarget.parentElement.parentElement
    const id = element.getAttribute("token-name")

    makeAPICall(`/token/${id}`, "GET").then((data) => {
        data = data[0]
        token.value = data.name
        ticker.value = data.ticker
        amountHeld.value = data.amountHeld
        address.value = data.accountAddress
        editFlag = true
        submitBtn.textContent = 'edit'
    })
}

function setBackToDefault() {
    token.value = ''
    ticker.value = ''
    amountHeld.value = ''
    editFlag = false
    editID = ''
    submitBtn.textContent = 'Add'
}

function setupItems(){
    const user = user_email.value
    makeAPICall(`/list-tokens`, "GET").then((data) => {
        // Sort by value
        // data.sort((a, b) => a.value - b.value);

        // Sort array by object name
        data.sort((a, b) => {
            const name1 = a.name.toUpperCase() // Ignore case
            const name2 = b.name.toUpperCase() // Ignore case
            if (name1 < name2) {
                return -1
            }
            if (name1 > name2) {
                return 1
            }
            return 0 // Should only happen if names are equal
        });

        // Add items to list in UI
        var totalPrice = 0
        if (data.length > 0) {
            data.forEach(item => {
                totalPrice += (item.price*item.amountHeld)
                createListItem(item.name, item.ticker, item.amountHeld, item.price, item.percent_change_7d)
            })
            container.classList.add('show-container')
            createTotalItem(numberWithCommas(totalPrice))
        }
    })
}

function createTotalItem(totalPrice) {
    const element = document.createElement('token')
    element.classList.add('token-item')
    const attr = document.createAttribute('token-name')
    attr.value = "Total"
    element.setAttributeNode(attr)

    element.innerHTML = `
            <p class="title">Total Price: <b><i style="color:green">$${totalPrice}</b></i>
            </p>
        `
    list.appendChild(element)
}

function createListItem(id, ticker, amount, price, percent_change_7d) {
    const element = document.createElement('token')
        element.classList.add('token-item')
        const attr = document.createAttribute('token-name')
        attr.value = id
        element.setAttributeNode(attr)
        totalPrice = numberWithCommas((amount*price))
        amount = numberWithCommas(amount)
        price = numberWithCommas(price)
        color = "green"
        if (percent_change_7d < 0) {
            color = "red"
        }
        element.innerHTML = `
            <p class="title">${ticker} <b><i style="color:${color}">${numberWithCommas(percent_change_7d)}%</b></i>
            <br>${amount} X $${price} = $${totalPrice}
            </p>
            <div class="btn-container">
                <button type='button' class='edit-btn'>
                    <i class='fas fa-edit'></i>
                </button>
                <button type='button' class='delete-btn'>
                    <i class='fas fa-trash'></i>
                </button>
            </div>
        `
        const deleteBtn = element.querySelector('.delete-btn')
        const editBtn = element.querySelector('.edit-btn')
        deleteBtn.addEventListener('click', deleteTodo)
        editBtn.addEventListener('click', editTodo)
        list.appendChild(element)
}

