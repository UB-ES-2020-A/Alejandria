$(document).ready(function () {

        var container = document.getElementById('container-products');
        var n_prods = document.getElementById('number-products');
        var i, total_price = 0;
        var titles = ['The Arrivals', 'The King of Drugs', 'No Place Like Here'];
        var prices = [15.95, 13.95, 24.95];
        for (i = 0; i < titles.length; i++) {
          create_info_price(titles[i], prices[i], '#', container);
          total_price += prices[i];
        }

        container.appendChild(document.createElement('HR'));

        var p_book = document.createElement('P');
        p_book.innerHTML = 'Total '

        var span_book = document.createElement('SPAN');
        span_book.className = 'price';
        span_book.style.color = 'black';

        var b_book = document.createElement('B');
        b_book.innerHTML = (total_price).toFixed(2) + ' €';

        p_book.appendChild(span_book);
        p_book.appendChild(b_book);
        container.appendChild(p_book)

        n_prods.innerHTML = titles.length;
    }
);

function create_info_price(title, price, url, container){
    var p_book = document.createElement('P');

    var a_book = document.createElement('A');
    a_book.href = url;
    a_book.innerHTML = title;

    var span_book = document.createElement('SPAN');
    span_book.className = 'price';
    span_book.innerHTML = price + ' €';

    p_book.appendChild(a_book);
    p_book.appendChild(span_book);
    container.appendChild(p_book);
}