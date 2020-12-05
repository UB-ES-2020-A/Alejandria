$(document).ready(function () {
    let data = null;
    let condition = false;

    $(".navbar-brand").click(function () {
        window.location.href = window.location.origin;
    });

    $("#home_btn").click(function () {
        window.location.href = window.location.origin;
    });

    $("#performLogout").click(function () {
        $("#logout_btn").click();
    })

    $("#buttonSearch").click(function () {
            book_name = document.getElementById('textSearch').value;
            if(book_name!=""){
                var urlname = window.location.origin+"/search";
                var url = new URL(urlname);
                url.searchParams.append('search_book', document.getElementById('textSearch').value);
                window.location.href = url;
            }
            else{ //TODO: Falta fer el search buit...
                console.log("NULL");
                window.location.href = "/search";
             }

        });

    $("#logout_btn").click(function () {
        var url = window.location.origin + "/login/";
        setCSRF();
        $.ajax(url, {
            method: "POST",
            data: {trigger: "logout"},
            ContentType: 'application/x-www-form-urlencode',
            success: function (response) {
                if (response.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong!',
                    })
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'See you later',
                        text: 'Logout was a success!',
                    })
                    $(".swal2-confirm").click(function () {
                        window.location.href = "";
                    });
                }
            }





        })
    });

    $("#forgot_btn_hidden").click(async function openForgotPasswordModal() {

        const {value: forgotParams} = await Swal.fire({
            title: "Forgot Password",
            html:
                '<input type="email" id="forgot_mail" class="swal2-input" placeholder="Enter email">'+
                '<small style="margin-right: 40%;">A Password Reset Email will be sent.</small>',

            showCancelButton: true,
            focusConfirm: false,
            preConfirm: () => {
                return {
                    mail: $("#forgot_mail").val(),
                    trigger: "forgot"

                }
            }
        })

        if (forgotParams) {
            var url = window.location.origin + "/forgot/";
            setCSRF();
            $.ajax(url, {
                method: "POST",
                data: forgotParams,
                ContentType: 'application/x-www-form-urlencode',
                success: function (response) {
                    if (response.error) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: response.msg,
                        })
                        $(".swal2-cancel").addClass("d-none")
                    } else {
                        Swal.fire({
                            icon: 'success',
                            title: response.msg,
                            text: 'Mail sent to your address',
                        })
                        $(".swal2-confirm").click(function () {
                            window.location.href = "";
                        });
                    }
                }

            })
        }
    });

    $("#login_btn").click(async function () {
        var url = window.location.origin + "/login/";

        const {value: loginParams} = await Swal.fire({
            title: "Sign In",
            html:
                '<div class="form-group">'+
                    '<label for="login_mail" style="margin-right: 100%;"><strong>Email</strong></label>'+
                    '<input type="email" id="login_mail" class="swal2-input" placeholder="Enter email">' +
                '</div>'+
                '<div class="form-group">'+
                    '<label for="login_password" style="margin-right: 100%;"><strong>Password</strong></label>'+
                    '<input type="password" id="login_password" class="swal2-input" placeholder="Enter password">' +
                '</div>'+
                '<a id="forgot_password" href="#" style="color:#dc3545!important; margin-right: 73%;" onclick="forgot_btn_hidden.click();"> <small> Forgot Password </small> <a>',
            showCancelButton: true,
            focusConfirm: false,
            preConfirm: () => {
                return {
                    mail: $("#login_mail").val(),
                    password: $("#login_password").val(),
                    trigger: "login"

                }
            }
        })

        if (loginParams) {
            setCSRF();
            $.ajax(url, {
                method: "POST",
                data: loginParams,
                ContentType: 'application/x-www-form-urlencode',
                success: function (response) {
                    if (response.error) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Something went wrong!',
                        })
                    } else {
                        Swal.fire({
                            icon: 'success',
                            title: 'Welcome back, ' + response.name,
                            text: 'Sign In was a success!',
                        })
                        $(".swal2-confirm").click(function () {
                            window.location.href = "";
                        });
                    }
                }

            })
        }
    });


    $("#faqs_btn").click(function () {
        window.location.href = "/faqs/";
    });

    $("#register_btn").click(function () {
        Swal.mixin({
            title: "Sign In",
            confirmButtonText: "Next &rarr;",
            progressSteps: ["1", "2", "3", "4"],
            showCancelButton: true,
            focusConfirm: false,
            allowOutsideClick: false,

        }).queue([
            {
                title: "Credentials and Personal Data",
                html:
                    '<div class="form-group">'+
                        '<label for="register_username" style="margin-right: 100%;"><strong>Username</strong></label>'+
                        '<input type="text" id="register_username" class="swal2-input form-control" placeholder="Username">' +
                        '<div class="alert alert-danger d-none" id="alertUsername" role="alert">The field is empty or already exists</div>'+
                        '<small id="usernameHelp" class="form-text text-muted" style="padding-right: 74%;">Displayed Name</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_firstname" style="margin-right: 77%;"><strong>First Name</strong></label>'+
                        '<input type="text" id="register_firstname" class="swal2-input form-control" placeholder="First Name">' +
                        '<div class="alert alert-danger d-none" id="alertFirstname" role="alert">The field is empty</div>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_lastname" style="margin-right: 77%;"><strong>Last Name</strong></label>'+
                        '<input type="text" id="register_lastname" class="swal2-input form-control" placeholder="Last Name">' +
                        '<div class="alert alert-danger d-none" id="alertLastname" role="alert">The field is empty or invalid</div>'+
                        '<small id="lastnameHelp" class="form-text text-muted" style="padding-right: 54%;">Please enter just 1 last name</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_email" style="margin-right: 69%;"><strong>Email Address</strong></label>'+
                        '<input type="email" id="register_email" class="swal2-input form-control" placeholder="Enter email">' +
                        '<div class="alert alert-danger d-none" id="alertEmail" role="alert">The field is empty or invalid or already exists</div>'+
                        '<small id="emailHelp" class="form-text text-muted" style="padding-right: 57%;">Enter a valid Email Address</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_password_1" style="margin-right: 100%;"><strong>Password</strong></label>'+
                        '<input type="password" id="register_password_1" class="swal2-input form-control" placeholder="Enter password">' +
                        '<div class="alert alert-danger d-none" id="alertPassword" role="alert">The field is empty</div>'+
                        '<small id="password1Help" class="form-text text-muted" style="padding-right: 32%;">Max. 50 characters. All characters are valid.</small>'+
                    '</div>',

                preConfirm: () => {
                    if(condition) {
                        condition = false;
                        return false;
                    }
                    data = {
                        username: $("#register_username").val(),
                        firstname: $("#register_firstname").val(),
                        lastname: $("#register_lastname").val(),
                        email: $("#register_email").val(),
                        password1: $("#register_password_1").val()
                    }

                    window.value = data;
                },
                willOpen: () => {
                    $(".swal2-confirm").click(function (event) {

                        if($("#register_username").val() == '') {
                            condition = true;
                            $("#alertUsername").removeClass("d-none");
                            setTimeout(function () {
                                $("#alertUsername").addClass("d-none");
                                if ($(".swal2-confirm")[0].disabled){
                                    $(".swal2-confirm")[0].disabled = false;
                                }
                                if ($(".swal2-cancel")[0].disabled){
                                    $(".swal2-cancel")[0].disabled = false;
                                }
                            },3000)

                        }

                        if($("#register_firstname").val() == '') {
                            condition = true;
                            $("#alertFirstname").removeClass("d-none");
                            setTimeout(function () {
                                $("#alertFirstname").addClass("d-none");
                                if ($(".swal2-confirm")[0].disabled){
                                    $(".swal2-confirm")[0].disabled = false;
                                }
                                if ($(".swal2-cancel")[0].disabled){
                                    $(".swal2-cancel")[0].disabled = false;
                                }
                            },3000)

                        }

                        if($("#register_lastname").val() == '' || $("#register_lastname").val().split(" ").length > 1) {
                            condition = true;
                            $("#alertLastname").removeClass("d-none");
                            setTimeout(function () {
                                $("#alertLastname").addClass("d-none");
                                if ($(".swal2-confirm")[0].disabled){
                                    $(".swal2-confirm")[0].disabled = false;
                                }
                                if ($(".swal2-cancel")[0].disabled){
                                    $(".swal2-cancel")[0].disabled = false;
                                }
                            },3000)

                        }

                        if($("#register_email").val() == '' || !validateEmail($("#register_email").val())) {
                            condition = true;
                            $("#alertEmail").removeClass("d-none");
                            setTimeout(function () {
                                $("#alertEmail").addClass("d-none");
                                if ($(".swal2-confirm")[0].disabled){
                                    $(".swal2-confirm")[0].disabled = false;
                                }
                                if ($(".swal2-cancel")[0].disabled){
                                    $(".swal2-cancel")[0].disabled = false;
                                }
                            },3000)

                        }

                        if($("#register_password_1").val() == '') {
                            condition = true;
                            $("#alertPassword").removeClass("d-none");
                            setTimeout(function () {
                                $("#alertPassword").addClass("d-none");

                                if ($(".swal2-confirm")[0].disabled){
                                    $(".swal2-confirm")[0].disabled = false;
                                }
                                if ($(".swal2-cancel")[0].disabled){
                                    $(".swal2-cancel")[0].disabled = false;
                                }
                            },3000);

                        }

                    })

                    $("#register_username").keyup(function () {
                        if ($("#register_username").val() != "") {
                            setCSRF();
                            $.ajax(window.location.origin+"/check/", {
                                method: "POST",
                                data: {username:$("#register_username").val()},
                                ContentType: 'application/x-www-form-urlencode',
                                success: function (response) {
                                    if (!response.exists){
                                        $("#alertUsername").addClass("d-none");
                                        $(".swal2-confirm")[0].disabled = false;
                                    }
                                    else {
                                        $("#alertUsername").removeClass("d-none");
                                        $(".swal2-confirm")[0].disabled = true;
                                    }
                                }

                            })
                        }

                    })

                    $("#register_email").keyup(function () {
                        if ($("#register_email").val() != "") {
                            setCSRF();
                            $.ajax(window.location.origin+"/check/", {
                                method: "POST",
                                data: {email:$("#register_email").val()},
                                ContentType: 'application/x-www-form-urlencode',
                                success: function (response) {
                                    if (!response.exists){
                                        $("#alertEmail").addClass("d-none");
                                        $(".swal2-confirm")[0].disabled = false;
                                    }
                                    else {
                                        $("#alertEmail").removeClass("d-none");
                                        $(".swal2-confirm")[0].disabled = true;

                                    }
                                }

                            })
                        }

                    })

                },
            },
            {
                title: "User Address",
                html:
                '<div class="form-group">'+
                    '<label for="register_country_1" style="margin-right: 100%;"><strong>Country</strong></label>'+
                    '<input type="text" id="register_country_1" class="swal2-input" placeholder="Country">' +
                '</div>'+

                '<div class="form-group">'+
                    '<label for="register_city_1" style="margin-right: 100%;"><strong>City</strong></label>'+
                    '<input type="text" id="register_city_1" class="swal2-input" placeholder="City">' +
                '</div>'+

                '<div class="form-group">'+
                    '<label for="register_street_1" style="margin-right: 100%;"><strong>Street</strong></label>'+
                    '<input type="text" id="register_street_1" class="swal2-input" placeholder="Street">' +
                '</div>'+

                '<div class="form-group">'+
                    '<label for="register_zip_1" style="margin-right: 81%;"><strong>Zip Code</strong></label>'+
                    '<input type="text" id="register_zip_1" class="swal2-input" placeholder="Zip Code">'+
                '</div>',

                preConfirm: () => {
                    data = {
                        country1: $("#register_country_1").val(),
                        city1: $("#register_city_1").val(),
                        street1: $("#register_street_1").val(),
                        zip1: $("#register_zip_1").val()
                    }
                    window.value = $.extend(window.value,data);
                }
            },
            {
                title: "Facturation Address",
                html:
                    '<div class="form-group">'+
                        '<label for="register_country_2" style="margin-right: 100%;"><strong>Country</strong></label>'+
                        '<input type="text" id="register_country_2" class="swal2-input" placeholder="Country">' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_city_2" style="margin-right: 100%;"><strong>City</strong></label>'+
                        '<input type="text" id="register_city_2" class="swal2-input" placeholder="City">' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_street_2" style="margin-right: 100%;"><strong>Street</strong></label>'+
                        '<input type="text" id="register_street_2" class="swal2-input" placeholder="Street">' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_zip_2" style="margin-right: 81%;"><strong>Zip Code</strong></label>'+
                        '<input type="text" id="register_zip_2" class="swal2-input" placeholder="Zip Code">'+
                    '</div>',
                preConfirm: () => {
                    data = {
                        country2: $("#register_country_2").val(),
                        city2: $("#register_city_2").val(),
                        street2: $("#register_street_2").val(),
                        zip2: $("#register_zip_2").val(),
                        trigger: "register"
                    }
                    window.value = $.extend(window.value,data);
                }
            },
            {
                title: "Give us your taste! (Optional)",
                html:
                    '<div class="form-group">'+
                        '<label for="genreDropdownBtn1" style="margin-right: 66%;"><strong>Your 1st choice</strong></label>'+
                        '<div class="dropdown">' +
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">Choose</button> '+
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
                            '</div> '+
                        '</div>' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="genreDropdownBtn2" style="margin-right: 66%;"><strong>Your 2nd choice</strong></label>'+
                        '<div class="dropdown">' +
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">Choose</button> '+
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
                            '</div> '+
                        '</div>' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="genreDropdownBtn3" style="margin-right: 66%;"><strong>Your 3rd choice</strong></label>'+
                        '<div class="dropdown">' +
                            '<button class="btn btn-secondary dropdown-toggle" type="button" id="genreDropdownBtn3" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-right: 100%;">Choose</button> '+
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
                            '</div> '+
                        '</div>' +
                    '</div>',
                preConfirm: () => {
                    let tastes = false;

                    if ($("#genreDropdownBtn1").text() != "Choose" || $("#genreDropdownBtn1").text() != "Choose" || $("#genreDropdownBtn1").text() != "Choose") {
                        tastes = true;
                    }

                    data = {
                        taste1: $("#genreDropdownBtn1").text(),
                        taste2: $("#genreDropdownBtn2").text(),
                        taste3: $("#genreDropdownBtn3").text(),
                        trigger: "register",
                        tastes: tastes
                    }
                    window.value = $.extend(window.value,data);
                },
                willOpen: () => {
                    $(".swal2-confirm").text("Send");

                    $(".item-taste-1").click(function () {
                        $("#genreDropdownBtn1").text($(this).text());
                        $("#genreDropdownBtn1").css("background-color","#dc3545");
                    })
                    $(".item-taste-2").click(function () {
                        $("#genreDropdownBtn2").text($(this).text());
                        $("#genreDropdownBtn2").css("background-color","#dc3545");
                    })
                    $(".item-taste-3").click(function () {
                        $("#genreDropdownBtn3").text($(this).text());
                        $("#genreDropdownBtn3").css("background-color","#dc3545");
                    })
                }
            }
        ]).then((result) => {
            var url = window.location.origin+"/register/"
            if(window.value){
                setCSRF();
                $.ajax(url, {
                    method: "POST",
                    data: window.value,
                    ContentType: 'application/x-www-form-urlencode',
                    success: function (response) {
                        if (response.error) {
                            window.value = ""
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                            })
                        } else {
                            Swal.fire({
                                icon: 'success',
                                allowOutsideClick: false,
                                title: 'Registered Successfully',
                                text: 'You can now Sign In to your account!',
                            })
                            $(".swal2-confirm").click(function () {
                                window.location.href = "";
                            });
                        }
                    }

                })
            }

        })
    });
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

function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}