$(document).ready(function () {
    $("#register_btn").click(function () {
        window.location.href = window.location.origin + "/register";
    });

    $(".navbar-brand").click(function () {
        window.location.href = window.location.origin;
    });

    $("#home_btn").click(function () {
        window.location.href = window.location.origin;
    });

    $("#logout_btn").click(function (){
        var url = window.location.origin+"/login/";
        setCSRF();
        $.ajax(url, {
                method: "POST",
                data: {trigger:"logout"},
                ContentType: 'application/x-www-form-urlencode',
                success: function (response) {
                    if(response.error){
                        Swal.fire({
                          icon: 'error',
                          title: 'Oops...',
                          text: 'Something went wrong!',
                        })
                    }
                    else{
                        Swal.fire({
                          icon: 'success',
                          title: 'See you later',
                          text: 'Logout was a success!',
                        })
                        $(".swal2-confirm").click(function(){ window.location.href = ""; });
                    }
                }

            })
    });

    $("#login_btn").click(async function () {
        var url = window.location.origin+"/login/";

        const { value: loginParams } = await Swal.fire({
            title: "Sign In",
            html:
                '<input type="email" id="login_mail" class="swal2-input" placeholder="Enter email">'+
                '<input type="password" id="login_password" class="swal2-input" placeholder="Enter password">'+
                '<a id="forgot_password" href=""> <small> Forgot Password </small> <a>',
            showCancelButton: true,
            focusConfirm: false,
            preConfirm: () => {
                return {
                    mail:$("#login_mail").val(),
                    password:$("#login_password").val(),
                    trigger:"login"

                }
            }
        })

        if(loginParams){
            setCSRF();
            $.ajax(url, {
                method: "POST",
                data: loginParams,
                ContentType: 'application/x-www-form-urlencode',
                success: function (response) {
                    if(response.error){
                        Swal.fire({
                          icon: 'error',
                          title: 'Oops...',
                          text: 'Something went wrong!',
                        })
                    }
                    else{
                        Swal.fire({
                          icon: 'success',
                          title: 'Welcome back, '+response.name,
                          text: 'Sign In was a success!',
                        })
                        $(".swal2-confirm").click(function(){ window.location.href = ""; });
                    }
                }

            })
        }
    });
});

function setCSRF() {
    $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                            // Only send the token to relative URLs i.e. locally.
                            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
                        }
                    }
                }
            });
}