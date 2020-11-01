$(document).ready(function () {
        $("#register_btn").click(function () {
            window.location.href = window.location.origin+"/register";
        });

        $(".navbar-brand").click(function () {
            window.location.href = window.location.origin;
        });

        $("#home_btn").click(function () {
            window.location.href = window.location.origin;
        });

        $("#login_btn").click(function () {
            window.location.href = window.location.origin+"/login";
        });

    }
);