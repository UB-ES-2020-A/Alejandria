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
            $("#text_name").val(full_name.join(" ").replace(/\n/ig, ''));
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
                username: username, first_name:first_name, last_name: last_name, email: email,
                street1: street1, city1: city1, country1: country1, zip1: zip1,
                street2: street2, city2: city2, country2: country2, zip2: zip2,
                taste1: taste1, taste2: taste2, taste3: taste3
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

function setCSRF() {
    function getCSRFToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;

    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
                //if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
                //}
            }
        }

    });
}