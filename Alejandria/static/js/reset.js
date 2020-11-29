$(document).ready(function () {
    $("#change_btn").click(function () {
        var password = $("#id_password").val();
        var password2 = $("#id_confirm").val();

        if (password != password2){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "Passwords do not match",
            });
            $("#id_password").val("");
            $("#id_confirm").val("");
        }
        else {
            var url = window.location.href
            setCSRF();
            $.ajax(url, {
                    method: "POST",
                    data: {new_pass:password, trigger:"reset"},
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
                                title: 'Password Changed!',
                                text: 'You can now Sign In to your account!',
                            })
                            $(".swal2-confirm").click(function () {
                                window.location.href = window.location.origin+"/";
                            });
                        }
                    }

                })

        }
    })
})