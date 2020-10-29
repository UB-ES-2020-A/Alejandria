function add_books_btn1() {
  var books = parseInt(document.getElementById("quantity_book_1").innerText);
  document.getElementById("quantity_book_1").innerHTML = books + 1;
  document.getElementById("quantity_sum_1").innerHTML = books + 1;
  updatePrices();
}

function add_books_btn2() {
  var books = parseInt(document.getElementById("quantity_book_2").innerText);
  document.getElementById("quantity_book_2").innerHTML = books + 1;
  document.getElementById("quantity_sum_2").innerHTML = books + 1;
  updatePrices();
}

function add_books_btn3() {
  var books = parseInt(document.getElementById("quantity_book_3").innerText);
  document.getElementById("quantity_book_3").innerHTML = books + 1;
  document.getElementById("quantity_sum_3").innerHTML = books + 1;
  updatePrices();
}

function updatePrices(){
  var price1 = parseFloat(document.getElementById("original_price_1").innerText);
  var price2 = parseFloat(document.getElementById("original_price_2").innerText);
  var price3 = parseFloat(document.getElementById("original_price_3").innerText);

  var books1 = parseInt(document.getElementById("quantity_book_1").innerText);
  var books2 = parseInt(document.getElementById("quantity_book_2").innerText);
  var books3 = parseInt(document.getElementById("quantity_book_3").innerText);

  document.getElementById("price_book_1").innerHTML = (books1 * price1).toFixed(2);
  document.getElementById("price_book_2").innerHTML = (books2 * price2).toFixed(2);
  document.getElementById("price_book_3").innerHTML = (books3 * price3).toFixed(2);
  document.getElementById("priceTotal").innerHTML = (books1 * price1 + books2 * price2 + books3 * price3).toFixed(2);
}