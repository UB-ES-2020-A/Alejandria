var total = 0.00; //Just for this example
var n_books = 0;

/*  Add function   */
function update_quantity(evt) {
  var price = evt.currentTarget.myParamPrice;
  var selectID = evt.currentTarget.myParamID;
  var books_remained = $('#' + selectID).val();
  var id_price = evt.currentTarget.myParamIDPrice;

  var n_books_selected = n_books_left(document.getElementById(id_price).innerHTML, books_remained * price, price);

  document.getElementById(id_price).innerHTML = (books_remained * price).toFixed(2) + '€';
  n_books = n_books + n_books_selected;
  total = total + n_books_selected * price;
  updatePrices();
}

function n_books_left(price_before, price_now, price) {
  price_before = price_before.substring(0, price_before.length - 1);
  return price_now / price - price_before / price
}


/*  Delete function    */
function dlt_books_btn(evt) {
  var price = evt.currentTarget.myParamPrice;
  var id_block = evt.currentTarget.myParamIDBook;
  var selectID = evt.currentTarget.myParamID;
  var books = $('#' + selectID).val();
  total = total - price * books;
  n_books = n_books - books;
  document.getElementById('container-info-books').removeChild(document.getElementById(id_block));
  updatePrices();
}

function updatePrices() {

  if (total == -0) {
    total = 0;
  }

  document.getElementById("priceTotal").innerHTML = (total).toFixed(2);
  document.getElementById("total_products").innerHTML = n_books;

  document.getElementById("priceSubtotal").innerHTML = (total).toFixed(2);
  document.getElementById("subtotal_products").innerHTML = n_books;

  document.getElementById("total_items_not").innerHTML = n_books;

  if (n_books == 1) {
    document.getElementById("products").innerHTML = 'product';
    document.getElementById("items").innerHTML = 'item';
  } else {
    document.getElementById("products").innerHTML = 'products';
    document.getElementById("items").innerHTML = 'items';
  }

}

function addToCart(new_price) {
  n_books = n_books + 1;
  total = total + new_price;
  updatePrices();
}