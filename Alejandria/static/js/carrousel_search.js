
$(document).ready(function () {
    console.log("hola");
    $.ajax({
            type: 'GET',
            dataType:'json',
            url: "get/ajax/books",//"{% url 'getAllBooks' %}",
            //data: {"nick_name": nick_name},
            success: function (response) {
                console.log("hola1");
                console.log(response);



            $.each(response['books'], function (i) {
                    console.log("HOLITA");
                    console.log(response['books'][i]);
                    console.log("HOLITA");
                    //console.log(response[i]);
                    //var attrs_book = response[i]["fields"];
                    //console.log(attrs_book);
                    var line_1 = '<div class="item" style="width: 185px;">';
                    var line_2 = '<div class="card" style="width: 11rem;">';
                    var book_href = "/book/" + response['books'][i]['ISBN'];
                    var line_3 = '<a href=' + book_href + ' style="text-decoration: none; color: inherit;">';
                    var line_4 = '<img class="card-img-top" src="https://imagessl6.casadellibro.com/a/l/t5/16/9788490667316.jpg" alt="Card image cap">'; //TODO: Change image;
                    var line_5 = '<div class="card-body">';
                    var line_6 = '<h5 class="card-title" style="padding-top:15px">' + response['books'][i]['title'] + '</h5>';
                    var line_7 = '<p class="card-text">' + 'Fernando Aramburu' + '</p>'; //TODO: CHANGE AUTHOR TO ONE;
                    var line_8 = ' <p class="card-text"> Preu: ' +  response['books'][i]['price'] + '€</p>';
                    var line_9 = '<a href="#" class="btn btn-primary">Afegir al carret</a>'; //TODO: Add to cart;
                    var line_10 = ' </div> </a> </div> </div>';
                    var card_str = line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7 + line_8 + line_9 + line_10;
                    $('#MultiCarouselCoincidents').append(card_str);







            })








            },
            error: function (response) {
                console.log("hola2");
                console.log(response);

            }
        })


})