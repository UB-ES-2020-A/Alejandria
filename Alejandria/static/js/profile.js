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

    $("#edit_btn").click(function () {
        if($("#edit_btn").html() != "Save Changes") {
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
            $("#id_country1").html('<input id="text_country1" type="text" class="form-control">');
            $("#text_country1").val(country1);
            $("#id_zip1").html('<input id="text_zip1" type="text" class="form-control">');
            $("#text_zip1").val(zip1);

            $("#id_street2").html('<input id="text_street2" type="text" class="form-control">');
            $("#text_street2").val(street2);
            $("#id_city2").html('<input id="text_city2" type="text" class="form-control">');
            $("#text_city2").val(city2);
            $("#id_country2").html('<input id="text_country2" type="text" class="form-control">');
            $("#text_country2").val(country2);
            $("#id_zip2").html('<input id="text_zip2" type="text" class="form-control">');
            $("#text_zip2").val(zip2);

            $("#id_taste1").html('<input id="text_taste1" type="text" class="form-control">');
            $("#text_taste1").val(taste1);
            $("#id_taste2").html('<input id="text_taste2" type="text" class="form-control">');
            $("#text_taste2").val(taste2);
            $("#id_taste3").html('<input id="text_taste3" type="text" class="form-control">');
            $("#text_taste3").val(taste3);

            $("#mainCard").height($("#profile").height());
            $("#tastes").height($("#facturation").height());
            $("#edit_btn").html("Save Changes");
        }
        else {
            var data = {
                username: $("#text_username").val(), full_name: $("#text_name").val(), email: $("#text_email").val(),
                street1: $("#text_street1").val(), city1: $("#text_city1").val(), country1: $("#text_country1").val(), zip1: $("#text_zip1").val(),
                street2: $("#text_street2").val(), city2: $("#text_city2").val(), country2: $("#text_country2").val(), zip2: $("#text_zip2").val(),
                taste1: $("#text_taste1").val(), taste2: $("#text_taste2").val(), taste3: $("#text_taste3").val()
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
                        Swal.fire({
                            icon: 'success',
                            title: 'Profile updated',
                            text: 'Your data has been modified!',
                        });
                    }
                    setTimeout(function () {
                            window.location.href = "";
                        },2000);
                }

            })

        }



    })



});
