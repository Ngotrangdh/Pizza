document.addEventListener('DOMContentLoaded', function () {
    let totalItems = parseInt(document.querySelector('#totalAddedItem').innerHTML);
    let currentToppingConstraint = 0;
    let currentSelectedVariantId = 0;
    let toppingIds = [];
    let addonIds = [];
    const toppingList = document.querySelectorAll('[name="topping"]');
    const addonList = document.querySelectorAll('[name="addon"]');

    // By defaul, the place order button is disabled
    const confirmCheckBox = document.querySelector('#order-confirm');
    const placeOrderButton = document.querySelector('#place-order-button');

    if (placeOrderButton) {
        placeOrderButton.disabled = true;
    }
    if (confirmCheckBox) {
        confirmCheckBox.onclick = () => {
            if (totalItems > 0 && confirmCheckBox.checked == true) {
                placeOrderButton.disabled = false;
            }
            else {
                placeOrderButton.disabled = true;
            }
        };
    }

    // Show modals when any price button is clicked
    document.querySelectorAll('[data-variantid]').forEach(function (button) {
        button.onclick = () => {
            toppingIds = [];
            addonIds = [];

            // By default, the addtocart button is disabled
            document.querySelector('.AddToCartButton').disabled = true;
            currentSelectedVariantId = button.dataset.variantid;
            currentToppingConstraint = parseInt(button.dataset.topping);
            if (currentToppingConstraint === 0) {
                document.querySelector('#exceedNumberToppingError').innerHTML = 'You cannot choose any toppings';
                document.querySelector('.AddToCartButton').disabled = false;
            } else {
                document.querySelector('#exceedNumberToppingError').innerHTML = '';
            }

            for (var i = 0; i < toppingList.length; i++) {
                toppingList[i].checked = false;
            }

            for (var i = 0; i < addonList.length; i++) {
                addonList[i].checked = false;
            }

            // Get the div .variantName and assign the selected product name
            document.querySelectorAll('.variantName').forEach((name) => {
                name.innerHTML = button.dataset.variantname;
            });
            document.querySelectorAll('.variantPrice').forEach((price) => {
                price.innerHTML = button.innerHTML;
            });
        };
    });


    // Validate number of chosen toppings then get a list of them if they're valid
    toppingList.forEach(function (checkbox) {
        checkbox.onclick = () => {
            toppingIds = [];
            document.querySelector('#exceedNumberToppingError').innerHTML = '';
            for (var i = 0; i < toppingList.length; i++) {
                if (toppingList[i].checked) {
                    toppingIds.push(toppingList[i].value);
                }
            }
            if (toppingIds.length != currentToppingConstraint) {
                if (currentToppingConstraint === 1) {
                    document.querySelector('#exceedNumberToppingError').innerHTML = `You have to choose one topping`;
                } else if (currentToppingConstraint === 0) {
                    document.querySelector('#exceedNumberToppingError').innerHTML = 'You cannot choose any toppings';
                } else {
                    document.querySelector(
                        '#exceedNumberToppingError'
                    ).innerHTML = `You have to choose ${currentToppingConstraint} toppings`;
                }
                document.querySelector('.AddToCartButton').disabled = true;
            } else {
                document.querySelector('.AddToCartButton').disabled = false;
            }
        };
    });

    // get a list of addons
    addonList.forEach(function (checkbox) {
        checkbox.onclick = () => {
            addonIds = [];
            for (var i = 0; i < addonList.length; i++) {
                if (addonList[i].checked) {
                    addonIds.push(addonList[i].value);
                }
            }
        };
    });

    // Define function getCookie and call it to get csrf token
    var csrftoken = getCookie('csrftoken');
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add items to shopping cart
    const buttons = document.querySelectorAll('.AddToCartButton');
    for (const button of buttons) {
        button.addEventListener('click', function () {
            const request = new XMLHttpRequest();
            const variantId = currentSelectedVariantId;

            request.open('POST', '/addtocart');
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.onload = () => {
                const info = JSON.parse(request.responseText);
                document.querySelector('#totalAddedItem').innerHTML = info.total;
            };
            const data = new FormData();
            data.append('toppings', toppingIds);
            data.append('addons', addonIds);
            data.append('id', variantId);
            request.send(data);
            // data.append('addons', Array
            // .from(document.querySelectorAll('[name="addon"]:checked'))
            // .map(checkbox => checkbox.value));
        });
    }

    // Update quantity in cart view
    document.querySelectorAll('.minus').forEach(button => {
        button.onclick = () => {
            let quantityButton = button.nextElementSibling;
            let currentQuantity = parseInt(quantityButton.innerHTML);
            if (currentQuantity <= 1) {
                currentQuantity = 1;
                return;
            }
            currentQuantity = currentQuantity - 1;
            const variantId = button.dataset.id;
            updateItemQuantity(variantId, currentQuantity);
            button.nextElementSibling.innerHTML = currentQuantity;
            document.querySelector('#totalAddedItem').innerHTML = totalItems - 1;
            totalItems = parseInt(document.querySelector('#totalAddedItem').innerHTML);
        }

    });

    document.querySelectorAll('.plus').forEach(function (button) {
        button.onclick = () => {
            let quantityButton = button.previousElementSibling;
            let currentQuantity = parseInt(quantityButton.innerHTML);
            currentQuantity = currentQuantity + 1
            const variantId = button.dataset.id;
            updateItemQuantity(variantId, currentQuantity);
            button.previousElementSibling.innerHTML = currentQuantity;
            document.querySelector('#totalAddedItem').innerHTML = totalItems + 1;
            totalItems = parseInt(document.querySelector('#totalAddedItem').innerHTML);
        };

    });

    // Function to send ajax request to update item quantity
    function updateItemQuantity(variantId, currentQuantity) {
        const request = new XMLHttpRequest();
        request.open('POST', '/updateitemquantity');
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.onload = () => {

        };
        const data = new FormData();
        data.append('id', variantId);
        data.append('quantity', currentQuantity);
        request.send(data);
    }

    // Delete items from cart
    document.querySelectorAll('.delete').forEach(function (button) {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            const variantId = button.dataset.id;
            request.open('POST', '/deletecart');
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.onload = () => {
                window.location.reload();
            };
            const data = new FormData();
            data.append('id', variantId);
            request.send(data);
        };

    });
});
