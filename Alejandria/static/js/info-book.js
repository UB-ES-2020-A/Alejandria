function createInfoBook(id_book, id_price, id_original_price, id_checkbox, id_quantity, id_btn_rmv, id_btn_add, var_title, var_author, var_rating, var_src_img, var_price) {

    var container = document.getElementById('container-info-books');
    var div_info_book = document.createElement('DIV');
    div_info_book.className = 'info-book';
    div_info_book.id = id_book;

    var img = document.createElement('IMG');
    img.className = 'book-cover';
    img.src = var_src_img;

    var div_mrg_left = document.createElement('DIV');
    div_mrg_left.style.marginLeft = '1%';

    var div_row = document.createElement('DIV');
    div_row.className = 'row horizontal';

    var div_col_1 = document.createElement('DIV');
    div_col_1.className = 'col';

    var p_title = document.createElement('P');
    p_title.className = 'book-title';

    var a_title = document.createElement('A');
    a_title.href = '#';
    a_title.innerHTML = var_title + ', by ' + var_author;

    var div_col_2 = document.createElement('DIV');
    div_col_2.className = 'col';

    var p_price = document.createElement('P');
    p_price.className = 'text';
    p_price.style.textAlign = 'right';

    var span_price = document.createElement('SPAN');
    span_price.id = id_price;
    span_price.innerHTML = var_price + '€';

    var p_original_price = document.createElement('P');
    p_original_price.className = 'price';
    p_original_price.id = id_original_price;
    p_original_price.innerHTML = var_price + '€';

    var div_checkbox = document.createElement('DIV');
    div_checkbox.className = 'custom-control custom-checkbox';

    var input_checkbox = document.createElement('INPUT');
    input_checkbox.className = 'custom-control-input';
    input_checkbox.type = 'checkbox';
    input_checkbox.id = id_checkbox;

    var label_checkbox = document.createElement('LABEL');
    label_checkbox.className = 'custom-control-label';
    label_checkbox.htmlFor  = id_checkbox;
    label_checkbox.style.color = 'white';
    label_checkbox.innerHTML = 'This is a gift';

    var span_rating = document.createElement("SPAN");
    span_rating.className = "score";
    span_rating.style.marginTop = "-5%";

    var div_wrap = document.createElement("DIV");
    div_wrap.className = "score-wrap";

    var span_stars = document.createElement("SPAN");
    span_stars.className = "stars-active";
    span_stars.style.width = var_rating + '%';

    var star_on = document.createElement("I");
    star_on.className = "fa fa-star";
    star_on.ariaHidden = "true";

    var span_stars_in = document.createElement("SPAN");
    span_stars_in.className = "stars-inactive";

    var star_off = document.createElement("I");
    star_off.className = "fa fa-star-o";
    star_off.ariaHidden = "false";

    var p_reviews = document.createElement('P');
    p_reviews.className = 'reviews';

    var a_reviews = document.createElement('A');
    a_reviews.href = '#';
    a_reviews.style.color = 'white';
    a_reviews.innerHTML = 'Reviews ';

    var span_not = document.createElement('SPAN');
    span_not.className = 'badge badge-light';
    span_not.style.fontSize = '0.7em';
    span_not.innerHTML = '15';

    var btn_rmv = document.createElement('BUTTON');
    btn_rmv.className = 'icon-btn add-btn';
    btn_rmv.id = id_btn_rmv;
    btn_rmv.style.marginTop = '5%';
    btn_rmv.onclick = 'rmv_books_btn1()';

    var div_text_rmv = document.createElement('DIV');
    div_text_rmv.className = 'btn_txt';
    div_text_rmv.innerHTML = 'Remove';

    var span_quantity = document.createElement('SPAN');
    span_quantity.style.color = 'white';
    span_quantity.style.fontSize = '14px';
    span_quantity.id = id_quantity;
    span_quantity.innerHTML = '1';

    var btn_add = document.createElement('BUTTON');
    btn_add.className = 'icon-btn add-btn';
    btn_add.id = id_btn_rmv;
    btn_add.style.marginTop = '5%';
    btn_add.onclick = 'add_books_btn1()';

    var div_add = document.createElement('DIV');
    div_add.className = 'add-icon';

    var div_text_add = document.createElement('DIV');
    div_text_add.className = 'btn_txt';
    div_text_add.innerHTML = 'Add';

    var div_pad_top = document.createElement('DIV');
    div_pad_top.style.paddingTop = '20%';

    var btn_delete = document.createElement('BUTTON');
    btn_delete.className = 'btn btn-outline-danger my-2 my-sm-0';
    btn_delete.onclick = 'dlt_books_btn1()';
    btn_delete.type = 'submit';
    btn_delete.innerHTML = 'Delete';

    var div_pad_bottom = document.createElement('DIV');
    div_pad_bottom.style.paddingBottom = '15%';

    /*  Construct Structure Info Book   */

    /*  Horizontal row  */
    p_title.appendChild(a_title);
    p_price.appendChild(span_price);
    div_col_1.appendChild(p_title);
    div_col_2.appendChild(p_price);
    div_row.appendChild(div_col_1);
    div_row.appendChild(div_col_2);
    /*  ./Horizontal row  */

    /*  Checkbox  */
    div_checkbox.appendChild(input_checkbox);
    div_checkbox.appendChild(label_checkbox);
    /*  ./Checkbox  */

    /*  Rating  */
    span_stars.appendChild(star_on);
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());

    span_stars_in.appendChild(star_off);
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());

    div_wrap.appendChild(span_stars);
    div_wrap.appendChild(span_stars_in);

    span_rating.appendChild(div_wrap);
    /*  ./Rating  */

    /*  Reviews  */
    a_reviews.appendChild(span_not);
    p_reviews.appendChild(a_reviews);
    /*  ./Reviews  */

    /*  Button Remove   */
    btn_rmv.appendChild(div_text_rmv);
    /*  ./Button Remove   */

    /*  Button Add   */
    btn_add.appendChild(div_add);
    btn_add.appendChild(div_text_add);
    /*  ./Button Add   */

    /*-------------------------------------------*/

    /*  Margin Left */
    div_mrg_left.appendChild(div_row);
    div_mrg_left.appendChild(p_original_price);
    div_mrg_left.appendChild(div_checkbox);
    div_mrg_left.appendChild(span_rating);
    div_mrg_left.appendChild(p_reviews);
    div_mrg_left.appendChild(btn_rmv);
    div_mrg_left.appendChild(span_quantity);
    div_mrg_left.appendChild(btn_add);
    div_mrg_left.appendChild(div_pad_top);
    div_mrg_left.appendChild(btn_delete);
    div_mrg_left.appendChild(div_pad_bottom);
    /*  ./Margin Left */

    /*-----------------------------------------*/

    /*  Div Info Book   */
    div_info_book.appendChild(img);
    div_info_book.appendChild(div_mrg_left);
    /*  Div Info Book   */

    container.insertBefore(div_info_book, container.firstChild);

    /*  ./Construct Structure Info Book   */
}