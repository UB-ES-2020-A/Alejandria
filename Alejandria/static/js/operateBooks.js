var total = 60.85; //Just for this example
var n_books = 3;

/*  Add function   */
function add_books_btn(evt) {
  var price = evt.currentTarget.myParamPrice;
  var id_books = evt.currentTarget.myParamIDQuantity;
  var books_remained = parseInt(document.getElementById(id_books).innerText);
  var id_price = evt.currentTarget.myParamIDPrice;
  document.getElementById(id_books).innerHTML = books_remained + 1;
  document.getElementById(id_price).innerHTML = (parseFloat(document.getElementById(id_price).innerText) + price).toFixed(2) + '€';
  n_books = n_books + 1;
  total = total + price;
  updatePrices();
}

/*  Remove function    */
function rmv_books_btn(evt) {
  var price = evt.currentTarget.myParamPrice;
  var id_books = evt.currentTarget.myParamIDQuantity;
  var id_price = evt.currentTarget.myParamIDPrice;
  var books_remained = parseInt(document.getElementById(id_books).innerText);
  if (books_remained > 0) {
    document.getElementById(id_books).innerHTML = books_remained - 1;
    document.getElementById(id_price).innerHTML = (parseFloat(document.getElementById(id_price).innerText) - price).toFixed(2) + '€';
    n_books = n_books - 1;
    total = total - price;
    updatePrices();
  }
}


/*  Delete function    */
function dlt_books_btn(evt) {
  var price = evt.currentTarget.myParamPrice;
  var id_books = evt.currentTarget.myParamIDQuantity;
  var id_block = evt.currentTarget.myParamIDBook;
  var books =  parseInt(document.getElementById(id_books).innerText);
  total = total - price * books;
  n_books = n_books - books;
  document.getElementById('container-info-books').removeChild(document.getElementById(id_block));
  updatePrices();
}

function updatePrices() {

  document.getElementById("priceTotal").innerHTML = (total).toFixed(2);
  document.getElementById("total_products").innerHTML = n_books;

  document.getElementById("priceSubtotal").innerHTML = (total).toFixed(2);
  document.getElementById("subtotal_products").innerHTML = n_books;

  if (n_books == 1) {
    document.getElementById("products").innerHTML = 'product';
    document.getElementById("items").innerHTML = 'item';
  } else {
    document.getElementById("products").innerHTML = 'products';
    document.getElementById("items").innerHTML = 'items';
  }

}