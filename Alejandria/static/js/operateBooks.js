var opt = 0;
var item_deleted = [false, false, false]

/*  Add functions   */
function add_books_btn1() {
  var books = parseInt(document.getElementById("quantity_book_1").innerText);
  document.getElementById("quantity_book_1").innerHTML = books + 1;
  updatePrices();
}

function add_books_btn2() {
  var books = parseInt(document.getElementById("quantity_book_2").innerText);
  document.getElementById("quantity_book_2").innerHTML = books + 1;
  updatePrices();
}

function add_books_btn3() {
  var books = parseInt(document.getElementById("quantity_book_3").innerText);
  document.getElementById("quantity_book_3").innerHTML = books + 1;
  updatePrices();
}

/*  Remove functions    */
function rmv_books_btn1() {
  var books = parseInt(document.getElementById("quantity_book_1").innerText);
  if (books > 0) {
    document.getElementById("quantity_book_1").innerHTML = books - 1;
  }
  updatePrices();
}

function rmv_books_btn2() {
  var books = parseInt(document.getElementById("quantity_book_2").innerText);
  if (books > 0) {
    document.getElementById("quantity_book_2").innerHTML = books - 1;
  }
  updatePrices();
}

function rmv_books_btn3() {
  var books = parseInt(document.getElementById("quantity_book_3").innerText);
  if (books > 0) {
    document.getElementById("quantity_book_3").innerHTML = books - 1;
  }
  updatePrices();
}

/*  Delete functions    */
function dlt_books_btn1() {
  opt = 1;
  updatePrices();
  document.getElementById("info_book_1").remove();
}

function dlt_books_btn2() {
  opt = 2;
  updatePrices();
  document.getElementById("info_book_2").remove();
}

function dlt_books_btn3() {
  opt = 3;
  updatePrices();
  document.getElementById("info_book_3").remove();
}

function updatePrices() {
  var price1 = 0;
  var price2 = 0;
  var price3 = 0;

  var books1 = 0;
  var books2 = 0;
  var books3 = 0;

  if (opt != 1 && !item_deleted[0]) {
    books1 = parseInt(document.getElementById("quantity_book_1").innerText);
    price1 = parseFloat(document.getElementById("original_price_1").innerText);
  }
  if (opt != 2 && !item_deleted[1]) {
    books2 = parseInt(document.getElementById("quantity_book_2").innerText);
    price2 = parseFloat(document.getElementById("original_price_2").innerText);
  }
  if (opt != 3 && !item_deleted[2]) {
    books3 = parseInt(document.getElementById("quantity_book_3").innerText);
    price3 = parseFloat(document.getElementById("original_price_3").innerText);
  }

  if (opt == 1 && !item_deleted[0]){
    item_deleted[0] = true;
  }
  if (opt == 2 && !item_deleted[1]){
    item_deleted[1] = true;
  }
  if (opt == 3 && !item_deleted[2]){
    item_deleted[2] = true;
  }

  if (!item_deleted[0])
    document.getElementById("price_book_1").innerHTML = (books1 * price1).toFixed(2);
  if (!item_deleted[1])
    document.getElementById("price_book_2").innerHTML = (books2 * price2).toFixed(2);
  if (!item_deleted[2])
    document.getElementById("price_book_3").innerHTML = (books3 * price3).toFixed(2);

  document.getElementById("priceTotal").innerHTML = (books1 * price1 + books2 * price2 + books3 * price3).toFixed(2);
  document.getElementById("total_products").innerHTML = books1 + books2 + books3;
  opt = 0;
}