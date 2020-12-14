$(document).ready(function () {
    // Rescale cards
    var property = "transform";
    var value = "translate(0%,15%)";
    $(".d-flex").css(property,value);
    $("#mainCard").height($("#profile").height());
    $("#tastes").height($("#facturation").height());

    // Retrieve Text from cards
    // User info
    let username = $("#id_username").html().split(" ").filter(item => !(item.length < 2))[0].replace(/\n/ig, '');
    let full_name = $("#id_name").html().split(" ").filter(item => !(item.length < 2));
    let first_name = full_name[0].replace(/\n/ig, '');
    let last_name = full_name[1].replace(/\n/ig, '');
    full_name = full_name.join(' ').replace(/\n/ig, '');
    let email = $("#id_email").html().split(" ").filter(item => !(item.length < 2))[0].replace(/\n/ig, '');
    let street1 = $("#id_street1").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let city1 = $("#id_city1").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let country1 = $("#id_country1").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let zip1 = $("#id_zip1").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    // Facturation Info
    let street2 = $("#id_street2").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let city2 = $("#id_city2").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let country2 = $("#id_country2").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    let zip2 = $("#id_zip2").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '');
    // Tastes Info
    let taste1 = $("#id_taste1").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '').replace("&amp;","&");
    let taste2 = $("#id_taste2").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '').replace("&amp;","&");
    let taste3 = $("#id_taste3").html().split(" ").filter(item => !(item.length < 2)).join(' ').replace(/\n/ig, '').replace("&amp;","&");

    
    $("#avatar-field").change(function () {
        readURL(this);
    });
    
    $("#avatar-2").click(function () {
        if($("#edit_btn").html() == "Save Changes"){
            $("#avatar-field").click();
        }
    });

    $("#edit_btn").click(function () {
        if($("#edit_btn").html() != "Save Changes") {
            $("#avatar-2").css("cursor", "pointer");
            $("#id_username").html('<input id="text_username" type="text" class="form-control">');
            $("#text_username").val(username);
            $("#id_name").html('<input id="text_name" type="text" class="form-control">');
            $("#text_name").val(full_name);
            $("#id_email").html('<input id="text_email" type="text" class="form-control">');
            $("#text_email").val(email);
            $("#id_street1").html('<input id="text_street1" type="text" class="form-control">');
            $("#text_street1").val(street1);
            $("#id_city1").html('<input id="text_city1" type="text" class="form-control">');
            $("#text_city1").val(city1);

            var html_country1 = '<button class="btn btn-secondary dropdown-toggle" type="button" id="countryDropdownBtn1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">Choose</button> '+
                            '<div class="dropdown-menu dropdown-menu-right" id="menu_country1" style="height: auto;max-height: 150px;overflow-x: hidden;" aria-labelledby="genreDropdownBtn1">' +
                            '</div> ';
            $("#id_country1").html(html_country1);
            $("#countryDropdownBtn1").text(country1);

            $("#id_zip1").html('<input id="text_zip1" type="text" class="form-control">');
            $("#text_zip1").val(zip1);

            $("#id_street2").html('<input id="text_street2" type="text" class="form-control">');
            $("#text_street2").val(street2);
            $("#id_city2").html('<input id="text_city2" type="text" class="form-control">');
            $("#text_city2").val(city2);

            var html_country2 = '<button class="btn btn-secondary dropdown-toggle" type="button" id="countryDropdownBtn2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">Choose</button> '+
                            '<div class="dropdown-menu dropdown-menu-right" id="menu_country2" style="height: auto;max-height: 150px;overflow-x: hidden;" aria-labelledby="genreDropdownBtn2">' +
                            '</div> ';
            $("#id_country2").html(html_country2);
            $("#countryDropdownBtn2").text(country2);

            $("#id_zip2").html('<input id="text_zip2" type="text" class="form-control">');
            $("#text_zip2").val(zip2);

            $.ajax("https://pkgstore.datahub.io/core/country-list/data_csv/data/d7c9d7cfb42cb69f4422dec222dbbaa8/data_csv.csv", {
                        method: "GET",
                        success: function (response) {
                            let data = response.split("\n");
                            data = data.slice(1,data.lenght);
                            let code1 = "";
                            let code2 = "";
                            let countries = data.map(parseData);


                            function parseData(value, index, array) {
                                let country = value.split(",")[0]
                                let html1 = '<a class="dropdown-item item-country-1" href="#">'+country.replace('"',"")+'</a>';
                                let html2 = '<a class="dropdown-item item-country-2" href="#">'+country.replace('"',"")+'</a>';
                                code1 += html1;
                                code2 += html2;
                                return html1;
                            }

                            $("#menu_country1").html(code1);
                            $("#menu_country2").html(code2);
                            $(".item-country-1").click(function () {
                                $("#countryDropdownBtn1").text($(this).text());
                                $("#countryDropdownBtn1").css("background-color","#dc3545");
                            })
                            $(".item-country-2").click(function () {
                                $("#countryDropdownBtn2").text($(this).text());
                                $("#countryDropdownBtn2").css("background-color","#dc3545");
                            })

                        }
                })

            var html1 = '<div class="form-group">'+
                        '<div class="dropdown">' +
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">'+taste1+'</button> '+
                            '<div class="dropdown-menu dropdown-menu-right" style="height: auto;max-height: 150px;overflow-x: hidden;" aria-labelledby="genreDropdownBtn1">' +
                                '<a class="dropdown-item item-taste-1" href="#">Fantasy</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Crime & Thriller</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Fiction</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Science Fiction</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Horror</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Romance</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Teen & Young Adult</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Children\'s Books</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Anime & Manga</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Others</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Art</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Biography</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Food</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">History</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Dictionary</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Health</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Humour</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Travel</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Sport</a> '+
                                '<a class="dropdown-item item-taste-1" href="#">Poetry</a> '+
                                '</div>'+
                            '</div>' +
                        '</div>';


            var html2 = '<div class="form-group">'+
                        '<div class="dropdown">' +
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">'+taste2+'</button> '+
                            '<div class="dropdown-menu dropdown-menu-right" style="height: auto;max-height: 150px;overflow-x: hidden;" aria-labelledby="genreDropdownBtn2">' +
                                '<a class="dropdown-item item-taste-2" href="#">Fantasy</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Crime & Thriller</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Fiction</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Science Fiction</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Horror</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Romance</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Teen & Young Adult</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Children\'s Books</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Anime & Manga</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Others</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Art</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Biography</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Food</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">History</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Dictionary</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Health</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Humour</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Travel</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Sport</a> '+
                                '<a class="dropdown-item item-taste-2" href="#">Poetry</a> '+
                                '</div>'+
                            '</div>' +
                        '</div>';


            var html3 = '<div class="form-group">'+
                        '<div class="dropdown">'+
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn3" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">'+taste1+'</button> '+
                            '<div class="dropdown-menu dropdown-menu-right" style="height: auto;max-height: 150px;overflow-x: hidden;" aria-labelledby="genreDropdownBtn3">' +
                                '<a class="dropdown-item item-taste-3" href="#">Fantasy</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Crime & Thriller</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Fiction</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Science Fiction</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Horror</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Romance</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Teen & Young Adult</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Children\'s Books</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Anime & Manga</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Others</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Art</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Biography</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Food</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">History</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Dictionary</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Health</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Humour</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Travel</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Sport</a> '+
                                '<a class="dropdown-item item-taste-3" href="#">Poetry</a> '+
                                '</div>'+
                            '</div>' +
                        '</div>';


            $("#id_taste1").html(html1);
            $("#id_taste2").html(html2);
            $("#id_taste3").html(html3);

            $(".item-taste-1").click(function () {
                $("#genreDropdownBtn1").text($(this).text());
                $("#genreDropdownBtn1").css("background-color","#dc3545");
            });

            $(".item-taste-2").click(function () {
                $("#genreDropdownBtn2").text($(this).text());
                $("#genreDropdownBtn2").css("background-color","#dc3545");
            });

            $(".item-taste-3").click(function () {
                $("#genreDropdownBtn3").text($(this).text());
                $("#genreDropdownBtn3").css("background-color","#dc3545");
            });



            $("#mainCard").height($("#profile").height());
            $("#tastes").height($("#facturation").height());

            $("#avatar-2").css("border", "5px solid #d9534f");
            $("#edit_btn").html("Save Changes");

        }
        else {
            $("#avatar-2").css("cursor", "pointer");
            var data = {
                username: $("#text_username").val(), full_name: $("#text_name").val(), email: $("#text_email").val(),
                street1: $("#text_street1").val(), city1: $("#text_city1").val(), country1: $("#countryDropdownBtn1").text(), zip1: $("#text_zip1").val(),
                street2: $("#text_street2").val(), city2: $("#text_city2").val(), country2: $("#countryDropdownBtn2").text(), zip2: $("#text_zip2").val(),
                taste1: $("#genreDropdownBtn1").text(), taste2: $("#genreDropdownBtn2").text(), taste3: $("#genreDropdownBtn3").text()
            };


            setCSRF();
            $.ajax(window.location.href,{
                method: "POST",
                data: data,
                ContentType: 'application/x-www-form-urlencode',
                success: function (response) {
                    if(response.error) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Something went wrong!',
                        })
                    }
                    else {
                        if ($("#avatar-field").val() != "") {
                            var dataForm = new FormData();
                            dataForm.append("avatar", $('#avatar-field')[0].files[0]);
                            dataForm.append("trigger", "avatar");
                            var status = navigator.sendBeacon(window.location.origin + "/avatar/", dataForm);
                        }
                        Swal.fire({
                            icon: 'success',
                            title: 'Profile updated',
                            text: 'Your data has been modified!',
                        });
                    }
                    setTimeout(function () {
                            window.location.href = "";
                        },2500);
                }
            });

        }



    })



});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#avatar-2').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}
