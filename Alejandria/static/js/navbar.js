$(document).ready(function () {
    let data = null;

    $(".navbar-brand").click(function () {
        window.location.href = window.location.origin;
    });

    $("#home_btn").click(function () {
        window.location.href = window.location.origin;
    });

    $("#buttonSearch").click(function () {
            book_name = document.getElementById('textSearch').value;
            if(book_name!=""){
                var urlname = window.location.origin+"/search";
                var url = new URL(urlname);
                url.searchParams.append('search_book', document.getElementById('textSearch').value);
                window.location.href = url;
                //window.location.href = "/search/" + document.getElementById('textSearch').value; //window.location.origin+"/login";
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

    /*return {


                }*/

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

        }).queue([
            {
                title: "Credentials and Personal Data",
                html:
                    '<div class="form-group">'+
                        '<label for="register_username" style="margin-right: 100%;"><strong>Username</strong></label>'+
                        '<input type="text" id="register_username" class="swal2-input form-control" placeholder="Username">' +
                        '<small id="usernameHelp" class="form-text text-muted" style="padding-right: 74%;">Displayed Name</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_firstname" style="margin-right: 77%;"><strong>First Name</strong></label>'+
                        '<input type="text" id="register_firstname" class="swal2-input form-control" placeholder="First Name">' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_lastname" style="margin-right: 77%;"><strong>Last Name</strong></label>'+
                        '<input type="text" id="register_lastname" class="swal2-input form-control" placeholder="Last Name">' +
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_email" style="margin-right: 69%;"><strong>Email Address</strong></label>'+
                        '<input type="email" id="register_email" class="swal2-input form-control" placeholder="Enter email">' +
                        '<small id="emailHelp" class="form-text text-muted" style="padding-right: 57%;">Enter a valid Email Address</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_password_1" style="margin-right: 100%;"><strong>Password</strong></label>'+
                        '<input type="password" id="register_password_1" class="swal2-input form-control" placeholder="Enter password">' +
                        '<small id="password1Help" class="form-text text-muted" style="padding-right: 32%;">Max. 50 characters. All characters are valid.</small>'+
                    '</div>'+

                    '<div class="form-group">'+
                        '<label for="register_password_2" style="margin-right: 61%;"><strong>Confirm Password</strong></label>'+
                        '<input type="password" id="register_password_2" class="swal2-input form-control" placeholder="Confirm password">'+
                        '<small id="password2Help" class="form-text text-muted" style="padding-right: 55%;">Both Passwords must match.</small>'+
                    '</div>',

                preConfirm: () => {
                    data = {
                        username: $("#register_username").val(),
                        firstname: $("#register_firstname").val(),
                        lastname: $("#register_lastname").val(),
                        email: $("#register_email").val(),
                        password1: $("#register_password_1").val(),
                        password2: $("#register_password_2").val()
                    }
                    window.value = data;
                }
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